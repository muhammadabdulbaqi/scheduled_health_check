
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

import os
import json
import smtplib
from email.message import EmailMessage

from rapidfuzz import fuzz

# === Load .env ===

EMAIL_USER = os.getenv("EMAIL_USER")  # e.g., m.abdulbaqi1702@gmail.com
EMAIL_PASS = os.getenv("EMAIL_PASS")  # Gmail password (NOT app password)
EMAIL_TO = os.getenv("EMAIL_TO")      # e.g., engineering@datasciencedojo.com

# === Config ===
QUERY_RESULTS_FILE = "evaluation_query_results.json"
OUTPUT_MATCHES_FILE = "fallback_matches.json"
FUZZY_THRESHOLD = 85

fallback_phrases = [
    "I don't have enough reliable information to answer this question accurately.",
    "Sorry, I cannot find the answer in the available sources."
]

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

def send_email(match_count):
    subject = "⚠️ RAI Health Check Fallback Detected"
    body = f"""
The health check returned {match_count} fallback-style responses. Please check service health — it may be down.

This is an automated alert from the evaluation monitoring system.
"""

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)
            print(f"✅ Alert email sent to {EMAIL_TO}")
    except Exception as e:
        print(f"❌ Failed to send alert email: {e}")

if __name__ == "__main__":
    matches = detect_fallbacks()
    if matches:
        send_email(len(matches))
