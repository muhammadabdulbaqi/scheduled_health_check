import os
import json
from azure.communication.email import EmailClient
from rapidfuzz import fuzz

# === Environment Variable Loader ===
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

# === Config ===
QUERY_RESULTS_FILE = "evaluation_query_results.json"
OUTPUT_MATCHES_FILE = "fallback_matches.json"
FUZZY_THRESHOLD = 85

fallback_phrases = [
    "I don't have enough reliable information to answer this question accurately.",
    "Sorry, I cannot find the answer in the available sources."
]

# === Fallback Detection ===
def detect_fallbacks():
    try:
        with open(QUERY_RESULTS_FILE, "r") as f:
            query_data = json.load(f)
            query_results = query_data.get("data", {}).get("query_results", [])
    except Exception as e:
        print(f"❌ Could not read {QUERY_RESULTS_FILE}: {e}")
        return []

    print(f"🔍 Loaded {len(query_results)} queries from {QUERY_RESULTS_FILE}\n")

    matches = []
    for q in query_results:
        generated = q.get("generated_response", "") or ""
        question = q.get("question", "")

        for phrase in fallback_phrases:
            similarity = fuzz.ratio(generated.lower(), phrase.lower())
            if similarity >= FUZZY_THRESHOLD:
                matches.append({
                    "question": question,
                    "generated_response": generated,
                    "matched_phrase": phrase,
                    "similarity": similarity
                })
                break

    if matches:
        with open(OUTPUT_MATCHES_FILE, "w") as f:
            json.dump(matches, f, indent=2)
        print(f"⚠️ Found {len(matches)} fallback-style responses.")
        print(f"📝 Matches written to {OUTPUT_MATCHES_FILE}")
    else:
        print("✅ No fallback-style responses detected.")
    return matches

# === Email Alert via ACS ===
def send_email():
    subject = "RAI Health Check Alert"
    plain_text = (
        "The health check returned an issue in the responses. "
        "Please check service health as it may be down."
    )

    try:
        connection_string = get_env_var("ACS_CONNECTION_STRING")
        sender = get_env_var("ACS_SENDER_EMAIL")
        recipient = get_env_var("ACS_RECIPIENT_EMAIL")

        client = EmailClient.from_connection_string(connection_string)
        message = {
            "senderAddress": sender,
            "recipients": {
                "to": [{"address": recipient}]
            },
            "content": {
                "subject": subject,
                "plainText": plain_text,
            },
        }

        poller = client.begin_send(message)
        result = poller.result()
        message_id = getattr(result, "message_id", "unknown")
        print(f"✅ Alert email sent. Message ID: {message_id}")

    except Exception as e:
        print(f"❌ Failed to send alert email: {e}")

# === Main ===
if __name__ == "__main__":
    matches = detect_fallbacks()
    if matches:
        send_email()
