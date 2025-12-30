from flask import Flask, request, render_template, jsonify
import os, time
from can_bus import CanRPC
from ota_agent import OTAAgent

app = Flask(__name__)
VEHICLE_ID = os.getenv("VEHICLE_ID", "VIN_SIM_0001")

# Initialize Shared CAN RPC
# Gateway Listen: 0x001 (Self) - but responses come to 0x101/0x201
can_rpc = CanRPC(0x001)

# Initialize OTA Agent
ota_agent = OTAAgent(VEHICLE_ID, can_rpc)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/approve", methods=["POST"])
def api_approve():
    data = request.json or {}
    simulate_failure = data.get("simulate_failure", False)
    
    ok, reason = ota_agent.approve_update(simulate_failure)
    if ok:
        return jsonify(ok=True)
    else:
        return jsonify(ok=False, error=reason)

@app.route("/api/vehicle/state", methods=["GET", "POST"])
def api_vehicle_state():
    if request.method == "POST":
        data = request.json or {}
        ota_agent.set_vehicle_state(data)
        return jsonify(ok=True)
    else:
        # Return defaults if not set
        if not hasattr(ota_agent, 'vehicle_state'):
             ota_agent.set_vehicle_state({})
        return jsonify(ota_agent.vehicle_state)

@app.route("/api/status", methods=["GET"])
def api_status():
    return jsonify({
        "approved": ota_agent.user_approved,
        "simulate_failure": getattr(ota_agent, "simulate_failure", False),
        "state": ota_agent.state,
        "job_id": ota_agent.job_id,
        "campaign_id": ota_agent.campaign_id,
        "details": {"reason": getattr(ota_agent, "failure_reason", None)} # Pass failure reason if any
    })

@app.route("/api/progress", methods=["GET"])
def api_progress():
    # Map agent progress to UI expectation
    # UI expects: {"engine": {percent...}, "adas": ...}
    # We'll simplify and show global progress for both ECUs for now, or spoof individual
    p = ota_agent.progress["percent"]
    status = ota_agent.progress["status"]
    
    prog_obj = {
        "engine": {"percent": p, "status": status, "current": p, "total": 100},
        "adas":   {"percent": p, "status": status, "current": p, "total": 100}
    }
    
    # We can add logs from a log buffer if we want, but for now just basic status
    return jsonify({"progress": prog_obj, "logs": [f"State: {ota_agent.state}"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
