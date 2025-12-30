import os, time, json, logging, threading, base64
import hashlib
import bsdiff4
from cryptography.hazmat.primitives.asymmetric import ed25519

from mqtt_client import OTAEventListener
from control_plane_client import ControlPlaneClient
from downloader import ArtifactDownloader
from trace_logger import TraceLogger

TRACER = TraceLogger("gateway")

# Constants
STATES = {
    "IDLE": "IDLE",
    "NOTIFIED": "NOTIFIED",
    "CONFIRMING": "CONFIRMING",
    "WAITING_FOR_APPROVAL": "WAITING_FOR_APPROVAL",
    "DOWNLOADING": "DOWNLOADING",
    "STAGED": "STAGED",
    "INSTALLING": "INSTALLING",
    "VALIDATING": "VALIDATING", 
    "SUCCEEDED": "SUCCEEDED",
    "FAILED": "FAILED",
    "STOPPED": "STOPPED",
    "ROLLED_BACK": "ROLLED_BACK"
}

ECUS = ["engine", "adas"]
CAN_IDS = {
    "engine": {"tx": 0x100, "rx": 0x101},
    "adas":   {"tx": 0x200, "rx": 0x201}
}

class OTAAgent:
    def __init__(self, vehicle_id, can_rpc):
        self.vehicle_id = vehicle_id
        self.can_rpc = can_rpc
        
        # Config
        self.cp_url = os.getenv("CONTROL_PLANE_URL", "http://control-plane:50051")
        self.broker = os.getenv("MQTT_BROKER", "mqtt")
        self.storage_path = "/tmp/ota_state.json"
        
        # Clients
        self.cp_client = ControlPlaneClient(vehicle_id)
        self.mqtt_listener = OTAEventListener(self.broker, vehicle_id, 
                                              on_notify=self.on_mqtt_notify,
                                              on_stop=self.on_mqtt_stop)
        self.downloader = ArtifactDownloader()
        
        # State
        self.state = STATES["IDLE"]
        self.job_id = None
        self.campaign_id = None
        self.manifest = None
        self.artifacts_map = {} # Loaded from manifest
        self.progress = {"percent": 0, "status": "Idle"}
        self.user_approved = False
        
        # Crypto
        # Hardcoding the public key for simulation (matches backend)
        # In prod this comes from secure storage or PKI
        self.backend_pub_key = ed25519.Ed25519PublicKey.from_public_bytes(
            base64.b64decode("BI/ezKPNG+EgSFCMkOnowq8sX8ZSnGZyN06cKtUxiss=")
        )
        
        # Load persisted state
        self.load_state()

        # Start Loop
        self.running = True
        self.thread = threading.Thread(target=self.loop)
        self.thread.start()
        
        # Start MQTT
        self.mqtt_listener.start()

    def load_state(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    self.state = data.get("state", STATES["IDLE"])
                    self.job_id = data.get("job_id")
                    self.campaign_id = data.get("campaign_id")
                    logging.info(f"Resumed state: {self.state}")
            except Exception as e:
                logging.error(f"Failed to load state: {e}")

    def save_state(self):
        data = {
            "state": self.state,
            "job_id": self.job_id,
            "campaign_id": self.campaign_id
        }
        with open(self.storage_path, 'w') as f:
            json.dump(data, f)

    def set_state(self, new_state, details=None):
        logging.info(f"State Transition: {self.state} -> {new_state}")
        TRACER.log("STATE_TRANSITION", {"from": self.state, "to": new_state, "details": details})
        self.state = new_state
        self.progress["status"] = new_state
        self.save_state()
        if self.job_id:
            self.cp_client.report_status(self.job_id, new_state, details)
        
        # Publish Heartbeat
        self.mqtt_listener.publish_heartbeat({
            "state": self.state,
            "job_id": self.job_id,
            "progress": self.progress["percent"]
        })

    def on_mqtt_notify(self, payload):
        logging.info(f"Received Notify: {payload}")
        if self.state in [STATES["IDLE"], STATES["SUCCEEDED"], STATES["FAILED"]]:
            # Trigger logic to check Control Plane
            self.campaign_candidate = payload.get("campaign_id")
            self.set_state(STATES["NOTIFIED"])

    def on_mqtt_stop(self, payload):
        logging.warning("Received Emergency Stop Signal!")
        # Pause everything
        prev_state = self.state
        
        # Confirm with CP
        try:
            policy = self.cp_client.confirm_emergency_stop(payload.get("stop_scope"), payload.get("nonce"))
            if policy.get("active"):
                self.set_state(STATES["STOPPED"])
            else:
                logging.info("Emergency Stop not confirmed by CP. Ignoring.")
        except Exception as e:
            logging.error(f"Failed to confirm stop: {e}")

    def set_vehicle_state(self, new_state):
        # Update internal state simulation
        if not hasattr(self, 'vehicle_state'):
             self.vehicle_state = {
                 "battery_soc": 50,
                 "gear": "P",
                 "parking_brake": True,
                 "ignition": "ON",
                 "speed": 0
             }
        self.vehicle_state.update(new_state)
        logging.info(f"Vehicle State Updated: {self.vehicle_state}")
        
    def check_preconditions(self):
        if not self.manifest: return False, "No Manifest"
        policy = self.manifest.get("policy", {})
        
        # Initialize defaults if not set
        if not hasattr(self, 'vehicle_state'):
             self.set_vehicle_state({})

        vs = self.vehicle_state
        
        # Check Battery
        min_soc = policy.get("min_battery_soc", 0)
        if vs["battery_soc"] < min_soc:
            return False, f"Battery too low ({vs['battery_soc']}% < {min_soc}%)"
            
        # Check Gear
        req_gear = policy.get("required_gear")
        if req_gear and vs["gear"] != req_gear:
            return False, f"Gear must be in {req_gear} (Current: {vs['gear']})"
            
        # Check Brake
        if policy.get("requires_parking_brake") and not vs["parking_brake"]:
             return False, "Parking Brake must be engaged"
             
        # Check Ignition
        req_ign = policy.get("requires_ignition_state")
        if req_ign and vs["ignition"] != req_ign:
             return False, f"Ignition must be {req_ign} (Current: {vs['ignition']})"
             
        return True, "OK"

    def approve_update(self, simulate_failure=False):
        if self.state == STATES["WAITING_FOR_APPROVAL"]:
            # Check Preconditions
            ok, reason = self.check_preconditions()
            if not ok:
                logging.warning(f"Approval Blocked: {reason}")
                return False, reason

            self.user_approved = True
            self.simulate_failure = simulate_failure
            logging.info("User approved update.")
            return True, "OK"
        return False, "Not in waiting state"

    def loop(self):
        while self.running:
            time.sleep(1)
            try:
                if self.state == STATES["NOTIFIED"]:
                    self.handle_notified()
                elif self.state == STATES["CONFIRMING"]:
                    self.handle_confirming()
                elif self.state == STATES["WAITING_FOR_APPROVAL"]:
                    if self.user_approved:
                        self.set_state(STATES["DOWNLOADING"])
                elif self.state == STATES["DOWNLOADING"]:
                    self.handle_downloading()
                elif self.state == STATES["STAGED"]:
                    self.handle_installing() # Auto proceed to install for sim simplicity, or check local gates
                elif self.state == STATES["INSTALLING"]:
                    pass # Handled in handle_installing which blocks or runs async
                elif self.state == STATES["VALIDATING"]:
                    pass
            except Exception as e:
                logging.error(f"Error in Agent Loop: {e}")
                # self.set_state(STATES["FAILED"], {"error": str(e)})

    def handle_notified(self):
        # Call CP to Confirm Eligibility and Get Job
        try:
            self.job_id = self.cp_client.create_or_resume_job(self.campaign_candidate)
            self.campaign_id = self.campaign_candidate
            self.set_state(STATES["CONFIRMING"])
        except Exception as e:
            logging.error(f"Failed to create job: {e}")
            self.set_state(STATES["IDLE"])

    def handle_confirming(self):
        # Get Manifest
        try:
            manifest_ref = f"manifest-{self.campaign_id}" # Simplified ref derivation
            data = self.cp_client.get_manifest(manifest_ref)
            
            # Verify Signature
            manifest = data["manifest"]
            signature = base64.b64decode(data["signature"])
            manifest_bytes = json.dumps(manifest, sort_keys=True).encode()
            
            try:
                self.backend_pub_key.verify(signature, manifest_bytes)
                logging.info("Manifest Signature Verified.")
            except Exception:
                logging.error("Manifest Signature Verification FAILED!")
                self.set_state(STATES["FAILED"], {"error": "Bad Manifest Sig"})
                return

            self.manifest = manifest
            self.set_state(STATES["WAITING_FOR_APPROVAL"])
        except Exception as e:
             logging.error(f"Failed to get/verify manifest: {e}")
             self.set_state(STATES["FAILED"])

    def handle_downloading(self):
        logging.info("Starting Downloads...")
        TRACER.log("DOWNLOAD_STARTED", {"campaign_id": self.campaign_id})
        self.progress["percent"] = 10
        
        # Process targets
        # For Sim, we need to download Delta, apply to V1 (cached), verify Result V2
        
        v1_cache = b"A" * 4096 # Mock V1
        
        for target in self.manifest["targets"]:
            ecu_id = target["ecu_id"]
            url = target["artifact_url"]
            expected_hash = target["artifact_hash"]
            # Download Delta patch
            local_path = f"/tmp/{ecu_id}_{self.campaign_id}.patch"
            
            if not self.downloader.download(url, local_path, None, None): # Hash check later for V2
                self.set_state(STATES["FAILED"], {"error": "Download Failed"})
                return

            # Apply Patch
            with open(local_path, 'rb') as f:
                patch_data = f.read()
            
            try:
                v2_data = bsdiff4.patch(v1_cache, patch_data)
                
                # Verify V2 Hash
                sha = hashlib.sha256(v2_data).hexdigest()
                if sha != expected_hash:
                    logging.error(f"Reconstructed Hash Mismatch! {sha} != {expected_hash}")
                    self.set_state(STATES["FAILED"], {"error": "Hash Mismatch"})
                    return
                
                # Store for Flashing
                self.artifacts_map[ecu_id] = v2_data
                logging.info(f"Artifact for {ecu_id} ready and verified.")
                TRACER.log("ARTIFACT_VERIFIED", {"ecu_id": ecu_id, "size": len(v2_data)})
            except Exception as e:
                 logging.error(f"Patching failed: {e}")
                 self.set_state(STATES["FAILED"])
                 return

        self.progress["percent"] = 50
        self.set_state(STATES["STAGED"])

    def handle_installing(self):
        self.set_state(STATES["INSTALLING"])
        self.progress["percent"] = 60
        
        # Flash Each ECU
        # In a real agent this would be more concurrent or robust
        for ecu_id, data in self.artifacts_map.items():
            if not self.flash_ecu(ecu_id, data):
                self.set_state(STATES["ROLLED_BACK"], {"reason": "ECU Flash Failed"})
                return
        
        self.set_state(STATES["VALIDATING"])
        # Final confirmation
        self.set_state(STATES["SUCCEEDED"])
        self.progress["percent"] = 100

    def flash_ecu(self, ecu_id, firmware_data):
        logging.info(f"Flashing {ecu_id}...")
        
        # 1. Enter Programming
        target = CAN_IDS[ecu_id]
        
        # Find target in manifest to get signature
        manifest_target = next((t for t in self.manifest["targets"] if t["ecu_id"] == ecu_id), None)
        if not manifest_target:
             logging.error(f"Target {ecu_id} not found in manifest")
             return False

        # Mock Meta for ECU (it expects some fields from old RPC)
        meta = {
            "vehicle_id": self.vehicle_id,
            "expected_size": len(firmware_data),
            "expected_sha256": hashlib.sha256(firmware_data).hexdigest(),
            "expected_signature": manifest_target.get("artifact_signature", ""),
        }
        
        # Send chunks
        self.can_rpc.send(target["tx"], "enter_programming", meta)
        ack = self.can_rpc.receive(target["rx"], timeout=2.0)
        if not ack:
             logging.error(f"ECU {ecu_id} No Ack to Enter Programming")
             return False

        off = 0
        while off < len(firmware_data):
             if self.state == STATES["STOPPED"]:
                 logging.error("Installation interrupted by Emergency Stop")
                 return False
                 
             chunk = firmware_data[off:off+512]
             self.can_rpc.send(target["tx"], "write_block", {
                 "offset": off,
                 "block_b64": base64.b64encode(chunk).decode()
             })
             ack = self.can_rpc.receive(target["rx"], timeout=3.0)
             if not ack:
                 logging.error(f"ECU {ecu_id} Write Timeout")
                 return False
             off += len(chunk)

        # Verify & Activate
        self.can_rpc.send(target["tx"], "verify", {"vehicle_id": self.vehicle_id})
        time.sleep(1)
        self.can_rpc.send(target["tx"], "activate", {"vehicle_id": self.vehicle_id, "simulate_failure": getattr(self, "simulate_failure", False)})
        self.can_rpc.send(target["tx"], "confirm", {"vehicle_id": self.vehicle_id})
        
        return True
