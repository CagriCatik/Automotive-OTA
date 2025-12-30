import json
import os
import datetime
import threading

# Default path inside containers
TRACE_FILE = os.getenv("TRACE_FILE_PATH", "/app/traces/simulation_trace.jsonl")

class TraceLogger:
    _lock = threading.Lock()

    def __init__(self, service_name):
        self.service_name = service_name

    def log(self, event_name, metadata=None):
        """
        Logs a structured event to the trace file.
        :param event_name: UpperSnakeCase event name (e.g. CAMPAIGN_STARTED)
        :param metadata: Dict of additional context
        """
        entry = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "service": self.service_name,
            "event": event_name,
            "metadata": metadata or {}
        }
        
        json_line = json.dumps(entry)
        
        # Print to stdout for Docker logs as well
        print(f"[TRACE] {json_line}")

        try:
            # Ensure dir exists (it should be mounted, but safe to check)
            os.makedirs(os.path.dirname(TRACE_FILE), exist_ok=True)
            
            # Simple file append with lock to prevent interleaved writes within same process
            # Note: Cross-process race conditions are possible but unlikely to corrupt 
            # the file significantly with append mode on a volume.
            with self._lock:
                with open(TRACE_FILE, "a") as f:
                    f.write(json_line + "\n")
        except Exception as e:
            print(f"FAILED TO WRITE TRACE: {e}")
