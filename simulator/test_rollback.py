import requests
import time

GATEWAY = "http://localhost:8080"

def test_rollback():
    print("1. Checking Status...")
    res = requests.get(f"{GATEWAY}/api/status").json()
    print(f"   Status: {res}")

    print("2. Simulating 'Simulate Bad Firmware' click...")
    # This triggers the rollback path
    requests.post(f"{GATEWAY}/api/approve", json={"simulate_failure": True})
    
    print("3. Polling Progress API (Expecting Failure/Rollback)...")
    last_status = {}
    for _ in range(20):
        res = requests.get(f"{GATEWAY}/api/progress").json()
        eng = res['progress']['engine']
        
        if eng['status'] != last_status.get('status'):
            print(f"   Engine State: {eng['status']}")
            last_status = eng
            
        # Log tail
        if res['logs']:
            print(f"   Log: {res['logs'][-1]}")
            
        time.sleep(1)

if __name__ == "__main__":
    test_rollback()
