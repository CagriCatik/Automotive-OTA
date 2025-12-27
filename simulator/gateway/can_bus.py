import can
import json
import time
import math

# Virtual CAN via UDP Multicast
# This allows containers to talk without a host network interface
BUS_CONFIG = {"interface": "udp_multicast", "channel": "239.0.0.1", "bitrate": 500000}

class CanRPC:
    def __init__(self, my_id):
        self.bus = can.Bus(**BUS_CONFIG)
        self.my_id = my_id # ID to listen for (simplified)

    def send(self, target_id, method, params):
        """
        Sends an RPC call as a sequence of CAN frames (Simulated ISO-TP).
        Format:
        Frame 0: [0xAA] [TotalFrames] [MethodLen] [Method...]
        Frame N: [0xBB] [SeqNum] [Data...]
        """
        payload = json.dumps({"m": method, "p": params}).encode('utf-8')
        
        # Split into chunks of 6 bytes (2 bytes header overhead)
        # Real CAN is 8 bytes.
        CHUNK_SIZE = 6
        total_chunks = math.ceil(len(payload) / CHUNK_SIZE)
        
        # 1. Send Start Frame
        # Header: [0xAA] [TotalChunks (1B)]
        # We assume TotalChunks < 255 for simulation simplicity
        # If payload is huge, this simple protocol breaks, but sufficient for our chunks
        
        # Actually, let's just use "Jumbo Frames" concept for simulation speed?
        # python-can udp_multicast supports larger sizes? 
        # Let's stick to strict 8-byte frames to prove the point of "CAN Bus".
        
        for i in range(total_chunks):
            chunk = payload[i*CHUNK_SIZE : (i+1)*CHUNK_SIZE]
            # Frame: [SeqNum] [MoreFlag] [Data...]
            # SeqNum: 0..255
            # MoreFlag: 1=More, 0=Last
            is_last = (i == total_chunks - 1)
            header = bytes([i % 255, 0 if is_last else 1])
            data = header + chunk
            
            # Pad to 8 bytes
            data = data.ljust(8, b'\x00')
            
            msg = can.Message(arbitration_id=target_id, data=data, is_extended_id=False)
            self.bus.send(msg)
            time.sleep(0.001) # Small delay to prevent UDP packet loss in Docker

    def receive(self, expected_id, timeout=None):
        """
        Blocks until a full JSON payload with arbitration_id == expected_id is received.
        """
        buffer = bytearray()
        started = False
        
        start_time = time.time()
        
        while True:
            # Check timeout
            if timeout and (time.time() - start_time > timeout):
                return None
                
            msg = self.bus.recv(0.1)
            if not msg: continue
            
            if msg.arbitration_id != expected_id:
                continue

            # Process Frame
            seq = msg.data[0]
            more = msg.data[1]
            chunk = msg.data[2:].rstrip(b'\x00') # Remove padding
            
            # Simple reassembly (naïve)
            buffer.extend(chunk)
            
            if more == 0:
                try:
                    return json.loads(buffer.decode('utf-8'))
                except:
                    buffer = bytearray() # Reset on error
                    
    def close(self):
        self.bus.shutdown()
