# OTA orchestrator (see README)
import requests, base64, hashlib, os, time
from cryptography.hazmat.primitives.asymmetric import ed25519

URL = os.getenv("VEHICLE_URL")
VID = os.getenv("VEHICLE_ID")
PRIV_KEY_B64 = os.getenv("OTA_SECRET_KEY")

priv_key = ed25519.Ed25519PrivateKey.from_private_bytes(base64.b64decode(PRIV_KEY_B64))

class OTAError(Exception): pass

def rpc(ecu, method, payload):
    try:
        resp = requests.post(f"{URL}/vehicle/ecus/{ecu}/rpc/{method}", json=payload)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("ok"):
            raise OTAError(f"ECU {ecu} rejected {method}: {data.get('error')}")
        print(f"[{ecu}] {method} OK")
    except Exception as e:
        raise OTAError(f"RPC failed: {e}")

# --- NEW: Polling for Driver Approval ---
print("Waiting for driver approval via Head Unit...")
simulate_failure = False
while True:
    try:
        # Check gateway status
        res = requests.get(f"{URL}/api/status")
        if res.ok:
            status = res.json()
            if status.get("approved"):
                simulate_failure = status.get("simulate_failure", False)
                print(f"Driver approved update! (Simulate Failure: {simulate_failure})")
                break
    except Exception:
        pass # Gateway might not be up yet
    time.sleep(2)
# ----------------------------------------

import bsdiff4

# ... (globals)

# Cache "Version 1" to serve as the base for the delta
# In a real scenario, this would be loaded from a database based on what the ECU reports it has.
v1_data = b"A" * 4096 
v2_data = os.urandom(4096)

for ecu in ["engine","adas"]:
    print(f"Starting update for {ecu}...")
    try:
        # Check if we should send a Delta
        # For simulation, we assume ECU has V1 and we want to send V2
        patch = bsdiff4.diff(v1_data, v2_data)
        print(f"Generated Delta Patch: {len(patch)} bytes (vs {len(v2_data)} bytes full)")

        sha = hashlib.sha256(v2_data).hexdigest()
        
        # Sign the hash of the TARGET (v2) firmware
        signature = priv_key.sign(sha.encode())
        sig_b64 = base64.b64encode(signature).decode()

        # Tell Gateway we are sending a patch
        rpc(ecu, "enter_programming", {
            "vehicle_id": VID,
            "expected_size": len(v2_data), # ECU expects full size
            "expected_sha256": sha,
            "expected_signature": sig_b64,
            "is_delta": True,
            "patch_size": len(patch)
        })

        # Send the PATCH
        off = 0
        while off < len(patch):
            chunk = patch[off:off+512]
            rpc(ecu, "write_block", {
                "vehicle_id": VID,
                "offset": off,
                "block_b64": base64.b64encode(chunk).decode()
            })
            off += len(chunk)
        
        # ... (verify/activate/confirm remains same)

        
        # 3. Verify Integrity & Authenticity
        rpc(ecu, "verify", {"vehicle_id": VID})

        # 4. Activate new firmware
        rpc(ecu, "activate", {
            "vehicle_id": VID,
            "simulate_failure": simulate_failure
        })
        rpc(ecu, "confirm", {"vehicle_id": VID})
        
        print(f"SUCCESS: {ecu} updated.")
    except OTAError as e:
        print(f"FAILED: {ecu} update aborted. Reason: {e}")
