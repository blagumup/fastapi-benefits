import imaplib
import base64
from models.supported_extensions import SupportedExtensions
from config import get_settings

settings = get_settings()

def connect_to_mailbox():
    """Connects to the IMAP mailbox and returns a mail object."""
    mail = imaplib.IMAP4_SSL(settings.EMAIL_HOST)
    mail.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
    mail.select("inbox")
    return mail

def fetch_unread_emails(mail):
    """Fetches unread emails and returns a list of email IDs."""
    status, email_ids = mail.search(None, "UNSEEN")
    return email_ids[0].split()

def extract_email_data(parsed_email):
    """Extracts subject, body, sender, and attachments from an email."""
    
    email_data = {
        "subject": parsed_email["subject"],
        "from": parsed_email["from"],
        "body": None,
        "attachments": []
    }

    # Extract email body (text/plain or text/html fallback)
    if parsed_email.is_multipart():
        for part in parsed_email.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            # Extract text body
            if content_type == "text/plain" and "attachment" not in content_disposition:
                email_data["body"] = part.get_payload(decode=True).decode(errors="ignore")

            # Extract attachments (PDFs, Images, etc.)
            if "attachment" in content_disposition:
                filename = part.get_filename()
                if filename:
                    file_data = part.get_payload(decode=True)
                    encoded_file = base64.b64encode(file_data).decode()  # Encode for easy transport
                    mime_type = _get_mime_type(filename)
                    email_data["attachments"].append({"filename": filename, "content": encoded_file, "mime_type": mime_type})

    # If plain text not found, try extracting from HTML
    if not email_data["body"]:
        for part in parsed_email.walk():
            if part.get_content_type() == "text/html":
                email_data["body"] = part.get_payload(decode=True).decode(errors="ignore")
                break  # Use the first HTML part found

    return email_data

def send_clarification_letter(user_email, mail_body):
    """Send letter to clarify information. Now use mock (print)"""
    print("Imitate sending clarification letter")
    print(mail_body)

def mark_email_as_read(mail, email_id):
    """Marks an email as read."""
    mail.store(email_id, "+FLAGS", "\\Seen")

def close_mailbox(mail):
    """Logs out and closes the mailbox connection."""
    mail.logout()

def _get_mime_type(filename):
    file_extension = filename.split('.', 1)[-1]
        
    try:
        mime_type = SupportedExtensions[file_extension.upper()].value
        print(f"Detected MIME type: {mime_type}")
    except:
        print(f"Unsupported file type: {file_extension}")
        mime_type = None
    return mime_type