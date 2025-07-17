import os
import time
import json
import requests
import subprocess
from dotenv import load_dotenv

# === Load ENV ===
load_dotenv()
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
HEADERS = {
    "Authorization": API_KEY,
    "Accept": "application/json"
}

# === Constants ===
EVAL_FILE = "latest_eval.json"
WAIT_INTERVAL = 20 * 60  # 20 minutes
MAX_ATTEMPTS = 6         # 6 x 20 mins = 2 hours

def get_eval_id():
    with open(EVAL_FILE, "r") as f:
        return json.load(f)["eval_run_id"]

def check_status(eval_id):
    url = f"{BASE_URL}/api/v2/evaluations/{eval_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"❌ Failed to fetch status. Code: {response.status_code}")
        return None
    return response.json().get("data", {}).get("status")

def wait_for_completion(eval_id):
    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"⏳ Attempt {attempt}/{MAX_ATTEMPTS}: Waiting {WAIT_INTERVAL//60} mins before checking evaluation status...")
        time.sleep(WAIT_INTERVAL)

        status = check_status(eval_id)
        print(f"🔄 Status after wait: {status}")

        if status == "completed":
            print("✅ Evaluation completed.")
            return True
        elif status not in ["pending", "running"]:
            print(f"❌ Unknown or failed status: {status}")
            return False

    print("❌ Evaluation did not complete within 2 hours. Stopping.")
    return False

def run_pipeline():
    print("🚀 Starting Evaluation Pipeline\n")

    # Step 1: Create evaluation
    subprocess.run(["python", "create_evaluation.py"], check=True)

    # Step 2: Load ID
    eval_id = get_eval_id()

    # Step 3: Wait for up to 2 hours
    if not wait_for_completion(eval_id):
        return

    # Step 4: Retrieve results
    subprocess.run(["python", "get_evaluation.py"], check=True)

    # Step 5: Detect fallbacks + alert
    subprocess.run(["python", "health_check_and_alert.py"], check=True)

if __name__ == "__main__":
    run_pipeline()
