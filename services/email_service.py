import asyncio
import email
import imaplib
from email import policy
import openai
from config import get_settings

settings = get_settings()

async def monitor_email():
    """Background task to continuously check for new emails."""
    while True:
        try:
            print("Checking inbox for new emails...")
            mail = imaplib.IMAP4_SSL(settings.EMAIL_HOST)
            mail.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
            mail.select("inbox")

            # Search for unread emails
            status, email_ids = mail.search(None, "UNSEEN")
            email_ids = email_ids[0].split()

            for e_id in email_ids:
                status, data = mail.fetch(e_id, "(RFC822)")
                raw_email = data[0][1]
                parsed_email = email.message_from_bytes(raw_email, policy=policy.default)
                
                # Process email text
                email_text = extract_email_text(parsed_email)
                print("Extracted email:", email_text)

                # Use GPT to parse text
                parsed_data = parse_with_gpt(email_text)
                print("Parsed Data:", parsed_data)

                # Mark email as seen
                mail.store(e_id, "+FLAGS", "\\Seen")

            mail.logout()
        except Exception as e:
            print("Error while checking email:", e)

        await asyncio.sleep(settings.CHECK_INTERVAL)  # Use config value


def extract_email_text(parsed_email):
    """Extracts plain text from email content."""
    if parsed_email.is_multipart():
        for part in parsed_email.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode()
    return parsed_email.get_payload(decode=True).decode()


def parse_with_gpt(text):
    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "Extract structured information from the receipt email. Respond in valid JSON format."},
            {"role": "user", "content": f"Extract the username, date, and receipt amount from this:\n{text}"}
        ],
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content


def get_system_prompt():
    return """"""