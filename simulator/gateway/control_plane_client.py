import os
import json
import logging
import grpc
import ota_pb2
import ota_pb2_grpc

CONTROL_PLANE_TARGET = os.getenv("CONTROL_PLANE_TARGET", "control-plane:50051")

class ControlPlaneClient:
    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        self.channel = grpc.insecure_channel(CONTROL_PLANE_TARGET)
        self.stub = ota_pb2_grpc.OtaControlStub(self.channel)
        logging.info(f"Connected to Control Plane at {CONTROL_PLANE_TARGET}")

    def check_in(self):
        try:
            req = ota_pb2.CheckInRequest(vehicle_id=self.vehicle_id)
            resp = self.stub.CheckIn(req)
            return resp.ok
        except grpc.RpcError as e:
            logging.error(f"CheckIn Failed: {e}")
            return False

    def get_manifest(self, manifest_ref):
        try:
            req = ota_pb2.GetManifestRequest(manifest_ref=manifest_ref)
            resp = self.stub.GetManifest(req)
            
            if resp.found:
                return {
                    "manifest": json.loads(resp.manifest_json),
                    "signature": resp.signature
                }
            return None
        except grpc.RpcError as e:
            logging.error(f"GetManifest Failed: {e}")
            return None

    def report_status(self, job_id, status, details=None):
        try:
            # Convert details to JSON string if dict
            d_str = json.dumps(details) if isinstance(details, dict) else str(details or "")
            
            req = ota_pb2.UpdateJobStatusRequest(
                job_id=job_id,
                status=status,
                details=d_str
            )
            self.stub.UpdateJobStatus(req)
            logging.info(f"Reported {status} for Job {job_id}")
            return True
        except grpc.RpcError as e:
            logging.error(f"ReportStatus Failed: {e}")
            return False

    def confirm_emergency_stop(self, request_id, status="STOPPED"):
        try:
            req = ota_pb2.ConfirmEmergencyStopRequest(
                request_id=request_id,
                vehicle_id=self.vehicle_id,
                status=status
            )
            self.stub.ConfirmEmergencyStop(req)
            return True
        except grpc.RpcError as e:
            logging.error(f"ConfirmStop Failed: {e}")
            return False

    def create_or_resume_job(self, campaign_id):
        try:
            req = ota_pb2.CreateJobRequest(
                campaign_id=campaign_id,
                vehicle_id=self.vehicle_id
            )
            resp = self.stub.CreateJob(req)
            if resp.created:
                logging.info(f"Job Created: {resp.job_id}")
                return resp.job_id
            return None
        except grpc.RpcError as e:
            logging.error(f"CreateJob Failed: {e}")
            raise
