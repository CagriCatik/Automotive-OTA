import grpc
from concurrent import futures
import time
import logging
import json
import ota_pb2
import ota_pb2_grpc
from trace_logger import TraceLogger

TRACER = TraceLogger("control-plane")

# Configure Logging
logging.basicConfig(level=logging.INFO)

# In-Memory Storage
JOBS = {}       # job_id -> {status, vehicle_id, ...}
MANIFESTS = {}  # manifest_ref -> {json, signature}
VEHICLES = {}   # vehicle_id -> last_checkin

class OtaControlServicer(ota_pb2_grpc.OtaControlServicer):
    
    def CheckIn(self, request, context):
        vid = request.vehicle_id
        VEHICLES[vid] = time.time()
        logging.info(f"CheckIn: {vid}")
        TRACER.log("VEHICLE_CHECKIN", {"vehicle_id": vid})
        return ota_pb2.CheckInResponse(ok=True)
    
    def RegisterManifest(self, request, context):
        ref = request.manifest_ref
        MANIFESTS[ref] = {
            "json": request.manifest_json,
            "signature": request.signature
        }
        logging.info(f"Registered Manifest: {ref}")
        return ota_pb2.RegisterManifestResponse(success=True, message="Stored")
    
    def UpdateJobStatus(self, request, context):
        job_id = request.job_id
        if job_id not in JOBS:
            JOBS[job_id] = {}
        JOBS[job_id]["status"] = request.status
        JOBS[job_id]["details"] = request.details
        
        logging.info(f"Job {job_id} -> {request.status}")
        TRACER.log("JOB_STATUS_UPDATE", {
            "job_id": job_id, 
            "status": request.status, 
            "details": request.details
        })
        return ota_pb2.UpdateJobStatusResponse(received=True)
    
    def GetManifest(self, request, context):
        ref = request.manifest_ref
        if ref in MANIFESTS:
            data = MANIFESTS[ref]
            return ota_pb2.GetManifestResponse(
                found=True,
                manifest_json=data["json"],
                signature=data["signature"]
            )
        else:
            return ota_pb2.GetManifestResponse(found=False)

    def ConfirmEmergencyStop(self, request, context):
        logging.warning(f"EMERGENCY STOP CONFIRMED by {request.vehicle_id}")
        TRACER.log("EMERGENCY_STOP_CONFIRMED", {"vehicle_id": request.vehicle_id})
        return ota_pb2.ConfirmEmergencyStopResponse(acknowledged=True)

    def CreateJob(self, request, context):
        # Simple job creation simulation
        import uuid
        job_id = f"job-{uuid.uuid4().hex[:8]}"
        
        JOBS[job_id] = {
            "status": "CREATED",
            "vehicle_id": request.vehicle_id,
            "campaign_id": request.campaign_id,
            "created_at": time.time()
        }
        
        logging.info(f"Created Job {job_id} for {request.vehicle_id} in {request.campaign_id}")
        TRACER.log("JOB_CREATED", {"job_id": job_id, "vehicle_id": request.vehicle_id, "campaign_id": request.campaign_id})
        
        return ota_pb2.CreateJobResponse(job_id=job_id, created=True)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ota_pb2_grpc.add_OtaControlServicer_to_server(OtaControlServicer(), server)
    server.add_insecure_port('[::]:50051')
    logging.info("Control Plane gRPC Server running on port 50051...")
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
