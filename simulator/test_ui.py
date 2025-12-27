import requests
import time

GATEWAY = "http://localhost:8080"

def test_ui_flow():
    print("1. Checking Status...")
    res = requests.get(f"{GATEWAY}/api/status").json()
    print(f"   Approved: {res['approved']}")

    print("2. Simulating 'Install Now' click...")
    requests.post(f"{GATEWAY}/api/approve", json={})
    
    print("3. Polling Progress API...")
    for _ in range(100):
        res = requests.get(f"{GATEWAY}/api/progress").json()
        eng = res['progress']['engine']
        print(f"   Engine: {eng['percent']}% ({eng['status']}) | Logs: {len(res['logs'])}")
        if eng['percent'] == 100:
            print("   SUCCESS: Engine reached 100%")
            print("--- LOGS ---")
            for l in res['logs']:
                print(l)
            print("------------")
            break
        time.sleep(1)

if __name__ == "__main__":
    try:
        test_ui_flow()
    except Exception as e:
        print(f"Test failed: {e}")
