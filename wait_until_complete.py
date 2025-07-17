
def get_env_var(key, required=True, json_parse=False, cast_int=False):
    value = os.getenv(key)
    if required and not value:
        raise ValueError(f"❌ Missing required environment variable: {key}")
    if json_parse:
        import json
        try:
            value = json.loads(value)
        except Exception as e:
            raise ValueError(f"❌ Failed to parse {key} as JSON: {e}")
    if cast_int:
        try:
            value = int(value)
        except Exception as e:
            raise ValueError(f"❌ Failed to cast {key} to int: {e}")
    return value

import time
import json
import requests
import os




BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
HEADERS = {
    "Authorization": API_KEY,
    "Accept": "application/json"
}

EVAL_FILE = "latest_eval.json"
WAIT_TIME = 20 * 60  # 20 minutes

def wait_then_check():
    # Step 1: Load eval ID
    with open(EVAL_FILE, "r") as f:
        eval_run_id = json.load(f)["eval_run_id"]

    print(f"⏳ Waiting {WAIT_TIME // 60} minutes before checking status of evaluation {eval_run_id}...")
    time.sleep(WAIT_TIME)

    # Step 2: Check status
    url = f"{BASE_URL}/api/v2/evaluations/{eval_run_id}"
    resp = requests.get(url, headers=HEADERS)

    if resp.status_code != 200:
        print(f"❌ Failed to check status: {resp.status_code}")
        return False

    status = resp.json().get("data", {}).get("status")
    print(f"🔄 Evaluation {eval_run_id} status after {WAIT_TIME//60} min: {status}")

    return status == "completed"

if __name__ == "__main__":
    if wait_then_check():
        print("✅ Evaluation is completed. Proceed.")
        exit(0)
    else:
        print("❌ Evaluation not completed in time.")
        exit(1)
