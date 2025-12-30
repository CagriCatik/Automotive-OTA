import requests, base64, hashlib, os, time, json, uuid
import paho.mqtt.client as mqtt
import bsdiff4
from cryptography.hazmat.primitives.asymmetric import ed25519

from cryptography.hazmat.primitives.asymmetric import ed25519
from trace_logger import TraceLogger

TRACER = TraceLogger("backend")

# Configuration
VEHICLE_ID = os.getenv("VEHICLE_ID", "VIN_SIM_0001")
CONTROL_PLANE_URL = os.getenv("CONTROL_PLANE_URL", "http://control-plane:50051")
ARTIFACT_SERVER_URL = os.getenv("ARTIFACT_SERVER_URL", "http://artifact-server:8082")
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt")
OTA_SECRET_KEY = os.getenv("OTA_SECRET_KEY")

# Setup Keys
priv_key = ed25519.Ed25519PrivateKey.from_private_bytes(base64.b64decode(OTA_SECRET_KEY))

def sign_data(data: bytes) -> str:
    return base64.b64encode(priv_key.sign(data)).decode()

def setup_artifacts(campaign_id):
    """Generates dummy firmware and delta paths."""
    print("Generating Artifacts...")
    base_dir = f"/app/artifacts/{campaign_id}"
    
    artifacts_map = {}
    
    for ecu in ["engine", "adas"]:
        ecu_dir = f"{base_dir}/{ecu}"
        os.makedirs(ecu_dir, exist_ok=True)
        
        # Simulate V1 (Base) and V2 (Target)
        v1_data = b"A" * 4096 
        v2_data = os.urandom(4096) # Random data for V2
        
        # Save V2 full
        with open(f"{ecu_dir}/full.bin", "wb") as f:
            f.write(v2_data)
            
        # Generate Delta
        patch = bsdiff4.diff(v1_data, v2_data)
        with open(f"{ecu_dir}/delta.patch", "wb") as f:
            f.write(patch)
            
        sha256 = hashlib.sha256(v2_data).hexdigest()

        # Sign the hash of the TARGET (v2) firmware
        signature = priv_key.sign(sha256.encode())
        sig_b64 = base64.b64encode(signature).decode()
        
        artifacts_map[ecu] = {
            "v2_sha256": sha256,
            "v2_signature": sig_b64,
            "v2_size": len(v2_data),
            "patch_size": len(patch),
            "delta_url": f"{ARTIFACT_SERVER_URL}/{campaign_id}/{ecu}/delta.patch",
            "full_url": f"{ARTIFACT_SERVER_URL}/{campaign_id}/{ecu}/full.bin"
        }
    return artifacts_map

def create_manifest(campaign_id, artifacts_map):
    manifest = {
        "schema_version": "1.0",
        "campaign_id": campaign_id,
        "manifest_ref": f"manifest-{campaign_id}",
        "created_at": time.time(),
        "expires_at": time.time() + 3600,
        "targets": [
            {
                "ecu_id": "engine",
                "component_name": "engine_ctrl",
                "base_version": "1.0",
                "target_version": "2.0",
                "artifact_type": "delta",
                "artifact_url": artifacts_map["engine"]["delta_url"],
                "artifact_size": artifacts_map["engine"]["patch_size"],
                "artifact_hash": artifacts_map["engine"]["v2_sha256"], # Target hash
                "artifact_signature": artifacts_map["engine"]["v2_signature"],
                "install_order": 1
            },
            {
                "ecu_id": "adas",
                "component_name": "adas_ctrl",
                "base_version": "1.0",
                "target_version": "2.0",
                "artifact_type": "delta",
                "artifact_url": artifacts_map["adas"]["delta_url"],
                "artifact_size": artifacts_map["adas"]["patch_size"],
                "artifact_hash": artifacts_map["adas"]["v2_sha256"],
                "artifact_signature": artifacts_map["adas"]["v2_signature"],
                "install_order": 1
            }
        ],
        "policy": {
            "requires_driver_approval": True,
            "requires_parked": True,
            "min_battery_soc": 20,
            "required_gear": "P",
            "requires_parking_brake": True,
            "requires_ignition_state": "ON"
        }
    }
    
    # Canonicalize and Sign
    manifest_bytes = json.dumps(manifest, sort_keys=True).encode()
    signature = sign_data(manifest_bytes)
    
    return {
        "manifest": manifest,
        "signature": signature,
        "manifest_ref": manifest["manifest_ref"]
    }

def register_manifest_cp(signed_manifest):
    import grpc
    import ota_pb2
    import ota_pb2_grpc
    
    target = os.getenv("CONTROL_PLANE_TARGET", "control-plane:50051")
    print(f"Connecting to Control Plane at {target}...")
    
    with grpc.insecure_channel(target) as channel:
        stub = ota_pb2_grpc.OtaControlStub(channel)
        req = ota_pb2.RegisterManifestRequest(
            manifest_json=json.dumps(signed_manifest["manifest"]),
            signature=signed_manifest["signature"],
            manifest_ref=signed_manifest["manifest_ref"]
        )
        try:
            resp = stub.RegisterManifest(req)
            if resp.success:
                print(f"Registered Manifest: {signed_manifest['manifest_ref']}")
                TRACER.log("MANIFEST_REGISTERED", {
                    "manifest_ref": signed_manifest['manifest_ref'],
                    "targets": len(signed_manifest['manifest']['targets'])
                })
            else:
                print(f"Registration Failed: {resp.message}")
        except grpc.RpcError as e:
            print(f"gRPC Failed: {e}")
            raise

def publish_notify(mqtt_client, campaign_id, manifest_ref):
    topic = f"v1/vehicles/{VEHICLE_ID}/ota/notify"
    payload = {
        "schema_version": "1.0",
        "campaign_id": campaign_id,
        "manifest_ref": manifest_ref,
        "priority": "normal",
        "not_before": time.time(),
        "expires_at": time.time() + 3600,
        "nonce": str(uuid.uuid4())
    }
    mqtt_client.publish(topic, json.dumps(payload))
    print(f"Published Notification to {topic}")
    TRACER.log("NOTIFICATION_PUBLISHED", {"topic": topic, "campaign_id": campaign_id})

def main():
    print("Backend Orchestrator Starting...")
    time.sleep(5) # Wait for services
    
    campaign_id = f"cam-{int(time.time())}"
    TRACER.log("CAMPAIGN_STARTED", {"campaign_id": campaign_id})
    
    # 1. Generate Artifacts
    artifacts_map = setup_artifacts(campaign_id)
    
    # 2. Create & Sign Manifest
    signed_manifest_data = create_manifest(campaign_id, artifacts_map)
    
    # 3. Register with Control Plane
    register_manifest_cp(signed_manifest_data)
    
    # 4. Connect MQTT
    client = mqtt.Client()
    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_start()
    
    # 5. Notify Vehicle
    time.sleep(2) # Give a moment
    publish_notify(client, campaign_id, signed_manifest_data["manifest_ref"])
    
    print("Campaign Launched. Monitoring...")
    
    # Keep alive and handle emergency stop simulation
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        client.loop_stop()

if __name__ == "__main__":
    main()
