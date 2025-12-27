from flask import Flask, request, render_template, jsonify
import os, requests, base64

app = Flask(__name__)
VEHICLE_ID = os.getenv("VEHICLE_ID")
from can_bus import CanRPC

# CAN Configuration
# Gateway Listen: 0x101 (Engine Reply), 0x201 (ADAS Reply) ?? No, it listens for specific replies.
# We don't really 'listen' globally, we request-response.
CAN_IDS = {
    "engine": {"tx": 0x100, "rx": 0x101},
    "adas":   {"tx": 0x200, "rx": 0x201}
}
# Initialize CAN (Gateway doesn't really have a 'my_id' if it initiates everything, but let's say 0x001)
can_rpc = CanRPC(0x001)

# Progress Tracking: {ecu_id: {percent: 0, status: "IDLE"}}
progress = {
    "engine": {"percent": 0, "status": "Waiting", "current": 0, "total": 1},
    "adas":   {"percent": 0, "status": "Waiting", "current": 0, "total": 1}
}
logs = []

# State: False = Pending, True = Approved
approval_state = {"approved": False, "simulate_failure": False}

def log(msg):
    print(msg, flush=True)
    logs.append(msg)
    if len(logs) > 50: logs.pop(0)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/approve", methods=["POST"])
def api_approve():
    data = request.json or {}
    approval_state["approved"] = True
    approval_state["simulate_failure"] = data.get("simulate_failure", False)
    
    if approval_state["simulate_failure"]:
        log("WARNING: Fault Injection Enabled. Expecting Rollback.")
    
    log("Driver authorized update.")
    return jsonify(ok=True)

@app.route("/api/status", methods=["GET"])
def api_status():
    return jsonify(approval_state)

@app.route("/api/progress", methods=["GET"])
def api_progress():
    return jsonify({"progress": progress, "logs": logs})

import bsdiff4
# Mock "Version 1" firmware that the vehicle already has
v1_cache = b"A" * 4096
patch_buffer = {}
metadata_buffer = {}

@app.route("/vehicle/ecus/<ecu>/rpc/<method>", methods=["POST"])
def route(ecu, method):
    data = request.json
    
    # Intercept for progress tracking & Delta Handling
    if method == "enter_programming":
        is_delta = data.get("is_delta", False)
        
        progress[ecu]["total"] = data.get("expected_size", 1)
        progress[ecu]["current"] = 0
        progress[ecu]["percent"] = 0
        progress[ecu]["status"] = "Flashing (Delta)..." if is_delta else "Flashing..."
        
        if is_delta:
            log(f"[{ecu}] Receiving Delta Patch ({data['patch_size']} bytes)...")
            patch_buffer[ecu] = bytearray()
            metadata_buffer[ecu] = data # Store for later
            return jsonify(ok=True) # Spoof success, buffering locally
        
        log(f"[{ecu}] Starting update (Size: {progress[ecu]['total']} bytes)")
    
    elif method == "write_block":
        # Check if we are in delta mode for this ECU
        if ecu in patch_buffer:
            chunk = base64.b64decode(data["block_b64"])
            patch_buffer[ecu].extend(chunk)
            progress[ecu]["percent"] = min(99, progress[ecu]["percent"] + 5)
            return jsonify(ok=True) # Spoof success

        # For normal write_block, we just fall through to send via CAN
        # Update progress estimate
        progress[ecu]["current"] += 512
        progress[ecu]["percent"] = min(99, int((progress[ecu]["current"] / progress[ecu]["total"]) * 100))

    elif method == "verify":
        if ecu in patch_buffer:
            log(f"[{ecu}] Reconstructing Firmware from Patch...")
            patch = bytes(patch_buffer[ecu])
            try:
                # Apply Patch
                v2_reconstructed = bsdiff4.patch(v1_cache, patch)
                log(f"[{ecu}] Patch Applied! (Size: {len(v2_reconstructed)})")
                
                # NOW send the full binary to the ECU via CAN
                full_data = v2_reconstructed
                
                if ecu not in metadata_buffer:
                     return jsonify(ok=False, error="Gateway Logic Error: Metadata lost during Delta Buffering")
                
                meta = metadata_buffer[ecu]
                # We strip 'is_delta' to avoid confusing ECU if it doesn't handle extra keys well
                # (though our ECU impl is robust, better safe)
                
                log(f"CAN TX -> {ecu}: enter_programming")
                target = CAN_IDS.get(ecu)
                can_rpc.send(target["tx"], "enter_programming", meta)
                
                # Wait for Ack (Enter Programming)
                ack = can_rpc.receive(target["rx"], timeout=2.0)
                log(f"DEBUG: Ack Received: {ack}")
                
                 # Permissive Check to debug
                if not ack:
                     return jsonify(ok=False, error=f"ECU {ecu} rejected enter_programming (CAN): No ACK")

                # 2. Send Chunks via CAN
                log(f"[{ecu}] Flashing Reconstructed Firmware over CAN...")
                off = 0
                while off < len(full_data):
                     chunk = full_data[off:off+512]
                     # Send write_block
                     can_rpc.send(target["tx"], "write_block", {
                         "offset": off,
                         "block_b64": base64.b64encode(chunk).decode()
                     })
                     # Wait for ACK
                     ack = can_rpc.receive(target["rx"], timeout=3.0) 
                     
                     if not ack:
                         return jsonify(ok=False, error=f"ECU Write Failure at {off}: No ACK")
                         
                     off += len(chunk)
                
                del patch_buffer[ecu]
                log(f"[{ecu}] Flashing Complete via CAN.")

            except Exception as e:
                log(f"[{ecu}] Patch Failed: {e}")
                return jsonify(ok=False, error=str(e))

        progress[ecu]["status"] = "Verifying Signatures..."
        log(f"[{ecu}] Verifying Ed25519 signatures...")
        
    elif method == "activate":
        progress[ecu]["status"] = "Activating..."
        progress[ecu]["percent"] = 100
        log(f"[{ecu}] Activating new firmware...")
        
    elif method == "confirm":
        progress[ecu]["status"] = "Update Complete"
        log(f"[{ecu}] Update successfully confirmed.")

    # --- CAN BUS BRIDGE ---
    target = CAN_IDS.get(ecu)
    if not target:
        return jsonify(ok=False, error="Unknown ECU")
        
    log(f"CAN TX -> {ecu}: {method}")
    # Send
    can_rpc.send(target["tx"], method, data)
    
    # Receive
    resp = can_rpc.receive(target["rx"], timeout=5.0)
    if not resp:
        return jsonify(ok=False, error="CAN Bus Timeout (ECU Unreachable)")
    
    # Unwrap 'p' (payload) if present
    if "p" in resp:
        resp = resp["p"]
        
    return jsonify(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
