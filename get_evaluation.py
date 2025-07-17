import os
import json
import requests
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

# === Load eval_run_id from file
try:
    with open("latest_eval.json", "r") as f:
        eval_run_id = json.load(f)["eval_run_id"]
except Exception as e:
    print(f"❌ Failed to read latest_eval.json: {e}")
    exit(1)

# === Headers
headers = {
    "Authorization": API_KEY,
    "Accept": "application/json"
}

# === Retrieve Evaluation Metadata ===
eval_url = f"{BASE_URL}/api/v2/evaluations/{eval_run_id}"
eval_response = requests.get(eval_url, headers=headers)

if eval_response.ok:
    eval_data = eval_response.json()
    print("✅ Evaluation metadata retrieved.")
    
    # Save to file
    with open("evaluation_metadata.json", "w") as f:
        json.dump(eval_data, f, indent=2)
    print("📝 Saved to evaluation_metadata.json")
else:
    print("❌ Failed to retrieve evaluation metadata:")
    print(eval_response.status_code, eval_response.text)
    exit(1)

# === Retrieve Query Results ===
query_url = f"{BASE_URL}/api/v2/evaluations/{eval_run_id}/query-results"
query_response = requests.get(query_url, headers=headers)

if query_response.ok:
    query_data = query_response.json()
    query_results = query_data.get("data", {}).get("query_results", [])
    
    print(f"✅ Retrieved {len(query_results)} query results.")
    
    # Save to file
    with open("evaluation_query_results.json", "w") as f:
        json.dump(query_data, f, indent=2)
    print("📝 Saved to evaluation_query_results.json")
    
    # Optional console output
    for i, q in enumerate(query_results, start=1):
        print(f"\n--- Query {i} ---")
        print(f"Question:           {q.get('question')}")
        print(f"Generated Response: {q.get('generated_response')}")
        print(f"Ground Truth:       {q.get('ground_truth')}")
        print("Metric Scores:")
        for m in q.get("metric_results", []):
            metric_name = m.get("metric_details", {}).get("display_name", "Unknown Metric")
            score = m.get("score")
            print(f"  - {metric_name}: {score}")
else:
    print("❌ Failed to retrieve query results:")
    print(query_response.status_code, query_response.text)
