import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# === Load environment variables from .env ===
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")  # Your Gmail
EMAIL_PASS = os.getenv("EMAIL_PASS")  # Your Gmail password
EMAIL_TO = "m.abdulbaqi1702@gmail.com"

def send_test_email():
    subject = "✅ Test Email from Python Script"
    body = """
This is a test email sent from a Python script using Gmail SMTP.
If you're reading this, the connection and login worked!
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
            print(f"✅ Test email sent to {EMAIL_TO}")
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")

if __name__ == "__main__":
    send_test_email()
