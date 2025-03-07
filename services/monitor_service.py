import asyncio
from email import policy, message_from_bytes
from services.mail_service import (
    connect_to_mailbox, fetch_unread_emails,
    extract_email_data, mark_email_as_read, close_mailbox
)
from services.open_ai_service import parse_with_gpt
import base64
from services.ocr_service import process_document_ocr
from models.ocr_processors import OCRProcessors
from config import get_settings

settings = get_settings()

async def monitor_new_benefit_requests():
    """Background task to continuously check for new emails."""
    while True:
        try:
            print("Checking inbox for new emails...")
            mail = connect_to_mailbox()

            # Get unread emails
            email_ids = fetch_unread_emails(mail)

            for e_id in email_ids:
                status, data = mail.fetch(e_id, "(RFC822)")
                raw_email = data[0][1]
                parsed_email = message_from_bytes(raw_email, policy=policy.default)  # ✅ FIXED

                # Extract structured email data
                email_data = extract_email_data(parsed_email)
                print("Extracted email:", email_data)
                
                # Extract text and entities from attachments using OCR
                for attachment in email_data["attachments"]:
                    attachment_content = base64.b64decode(attachment["content"])
                    mime_type = attachment["mime_type"]
                    # Using Custom Processor for OCR
                    attachment_text, attachment_entities = process_document_ocr(processor_id=OCRProcessors.CUSTOM_PARSER.value, file=attachment_content, mime_type=mime_type)
                    """
                    ADD LOGIC FOR FURTHER PROCESSING OF ATTACHMENT TEXT AND ENTITIES
                    """

                # Use GPT to parse text
                parsed_data = parse_with_gpt(email_data)
                print("Parsed Data:", parsed_data)

                #validate_request_data(parsed_data)

                # Save parsed data to DB
                save_benefit_request(parsed_data)

                # Mark email as seen
                mark_email_as_read(mail, e_id)

            close_mailbox(mail)
        except Exception as e:
            print("Error while checking email:", e)

        await asyncio.sleep(settings.CHECK_INTERVAL)  # Use config value
