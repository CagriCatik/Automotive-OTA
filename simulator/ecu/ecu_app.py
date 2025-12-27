import os, time, base64, hashlib, sys
from cryptography.hazmat.primitives.asymmetric import ed25519
from can_bus import CanRPC

# Configuration
ECU_ID = os.getenv("ECU_ID") # "engine" or "adas"
PUB_KEY_B64 = os.getenv("OTA_PUBLIC_KEY")

# CAN IDs
# Engine: Listen 0x100, Reply 0x101
# ADAS:   Listen 0x200, Reply 0x201
CAN_IDS = {
    "engine": 0x100,
    "adas":   0x200
}
LISTEN_ID = CAN_IDS.get(ECU_ID, 0x000)
REPLY_ID  = LISTEN_ID + 1

if LISTEN_ID == 0:
    print(f"Unknown ECU ID: {ECU_ID}")
    sys.exit(1)

print(f"ECU {ECU_ID} starting on CAN Bus (Listen: {hex(LISTEN_ID)})...")

# State Machine
state = {
    "mode": "IDLE", # IDLE, PROGRAMMING, VERIFIED, ACTIVATED, CONFIRMED
    "buffer": bytearray(),
    "expected_size": 0,
    "expected_sha256": None,
    "expected_signature": None
}

slots = {"current": "A", "target": "B"}
versions = {"A": "1.0.0", "B": None}
pub_key = ed25519.Ed25519PublicKey.from_public_bytes(base64.b64decode(PUB_KEY_B64))

can_rpc = CanRPC(LISTEN_ID)

def fail(reason):
    print(f"ERROR: {reason}")
    return {"ok": False, "error": reason}

def success():
    return {"ok": True}

def handle_rpc(method, params):
    global state
    print(f"RPC: {method}")
    
    if method == "enter_programming":
        params = params or {}
        state["mode"] = "PROGRAMMING"
        state["buffer"] = bytearray()
        state["expected_size"] = params.get("expected_size")
        state["expected_sha256"] = params.get("expected_sha256")
        state["expected_signature"] = params.get("expected_signature")
        return success()
        
    elif method == "write_block":
        if state["mode"] != "PROGRAMMING":
            return fail("bad state")
        
        offset = params.get("offset")
        block = base64.b64decode(params.get("block_b64"))
        
        # Simple buffer management (extend or overwrite)
        # In this sim, we just append assuming order, or use offset
        if len(state["buffer"]) < offset:
            state["buffer"].extend(b'\x00' * (offset - len(state["buffer"])))
        state["buffer"][offset:offset+len(block)] = block
        return success()
        
    elif method == "verify":
        if state["mode"] != "PROGRAMMING":
            return fail("bad state")
            
        # 1. Check SHA256 of firmware
        h = hashlib.sha256(state["buffer"]).hexdigest()
        if h != state["expected_sha256"]:
            state["mode"] = "IDLE"
            return fail("sha mismatch")
            
        # 2. Check Ed25519 Signature
        try:
            sig = base64.b64decode(state["expected_signature"])
            pub_key.verify(sig, state["expected_sha256"].encode())
        except Exception as e:
            state["mode"] = "IDLE"
            return fail(f"signature invalid: {e}")
            
        state["mode"] = "VERIFIED"
        return success()
        
    elif method == "activate":
        simulate_failure = params.get("simulate_failure", False)
        if state["mode"] != "VERIFIED":
            return fail("bad state")
            
        if simulate_failure:
            state["mode"] = "IDLE"
            return fail("Boot loop detected. Rolled back.")
            
        # Swap slots
        slots["current"], slots["target"] = slots["target"], slots["current"]
        state["mode"] = "ACTIVATED"
        return success()
        
    elif method == "confirm":
        if state["mode"] != "ACTIVATED":
            return fail("bad state")
        state["mode"] = "CONFIRMED"
        return success()
        
    return fail("method not found")

# Main Loop
while True:
    req = can_rpc.receive(LISTEN_ID)
    if req:
        resp = handle_rpc(req.get("m"), req.get("p"))
        can_rpc.send(REPLY_ID, "response", resp)
