import os
from azure.communication.email import EmailClient
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()

ACS_CONNECTION_STRING = os.getenv("ACS_CONNECTION_STRING")
ACS_SENDER_EMAIL = os.getenv("ACS_SENDER_EMAIL")
ACS_RECIPIENT_EMAIL = os.getenv("ACS_RECIPIENT_EMAIL")

def send_test_email():
    try:
        client = EmailClient.from_connection_string(ACS_CONNECTION_STRING)

        message = {
            "senderAddress": ACS_SENDER_EMAIL,
            "recipients": {
                "to": [{"address": ACS_RECIPIENT_EMAIL}]
            },
            "content": {
                "subject": "✅ Test Email from Azure Communication Services",
                "plainText": "Hello! This is a test email using Azure Communication Services.",
                "html": """
                <html>
                    <body>
                        <h2>Hello from Azure!</h2>
                        <p>This email was sent from a Python script using Azure Communication Services.</p>
                    </body>
                </html>
                """
            },
        }

        poller = client.begin_send(message)
        result = poller.result()
        message_id = result.get("messageId") or result.get("message_id", "unknown")
        print(f"✅ Email sent successfully. Message ID: {message_id}")

    except Exception as ex:
        print("❌ Failed to send email:", ex)

if __name__ == "__main__":
    send_test_email()
