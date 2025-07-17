import os
import json
import requests
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
AGENT_ID = int(os.getenv("AGENT_ID"))
DATASET_IDS = json.loads(os.getenv("DATASET_IDS"))  # Must be valid JSON list
METRIC_IDS = json.loads(os.getenv("METRIC_IDS"))

# === Endpoint ===
url = f"{BASE_URL}/api/v2/agents/{AGENT_ID}/evaluations"

# === Payload ===
payload = {
    "agent_id": AGENT_ID,
    "dataset_ids": DATASET_IDS,
    "metric_ids": METRIC_IDS,
    "evaluation_name": "Auto Evaluation - Python Script"
}

# === Headers ===
headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# === Send POST request ===
response = requests.post(url, headers=headers, json=payload)

# === Output and Save ID
if response.ok:
    result = response.json()
    print("✅ Evaluation created successfully:")
    print(json.dumps(result, indent=2))
    
    # Save eval_run_id to file
    eval_id = result["data"]["id"]
    with open("latest_eval.json", "w") as f:
        json.dump({"eval_run_id": eval_id}, f)
    print(f"📝 Evaluation ID saved to latest_eval.json: {eval_id}")
else:
    print("❌ Failed to create evaluation:")
    print(f"Status Code: {response.status_code}")
    print(response.text)
