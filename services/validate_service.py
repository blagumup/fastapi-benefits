import json  # ✅ Import JSON module
from typing import List, Dict
from datetime import datetime
from models.compensation_status import CompensationStatus
from services.mail_service import send_clarification_letter

REQUIRED_FIELDS = ["file_name", "category", "username", "document_number", "document_date", "document_sum", "document_currency", "account_number"]

def validate_and_set_status(user_email, parsed_data: str) -> Dict:
    """
    Parses JSON string, validates parsed OCR data, updates each item with `status_id`, and converts date format.

    Status IDs:
    - `1`: Data is complete ✅ (OPEN)
    - `2`: Data is missing required fields and needs clarification ❌ (WAITING_FOR_CLARIFICATION)

    Returns:
    - Updated dictionary with `status_id` added to each document.
    """
    try:
        parsed_data = json.loads(parsed_data)  # ✅ Convert JSON string to dictionary
    except json.JSONDecodeError as e:
        print(f"❌ JSON Parsing Error: {e}")
        return {}  # Return an empty dictionary if parsing fails

    invalid_records = []
    documents = parsed_data.get("documents", [])

    if not isinstance(documents, list):  # ✅ Ensure `documents` is a list
        print("❌ Error: `documents` is not a list! Data received:", documents)
        return parsed_data  # Return original data without changes

    for record in documents:
        if not isinstance(record, dict):  # ✅ Ensure each document is a dictionary
            print(f"❌ Error: Invalid record format! Expected dict but got: {type(record)} → {record}")
            continue  # Skip invalid records

        # ✅ Convert date format before validation
        if "document_date" in record and record["document_date"]:
            record["document_date"] = convert_date_format(record["document_date"])

        missing_fields = [field for field in REQUIRED_FIELDS if not record.get(field)]

        # Assign status based on missing fields
        if missing_fields:
            record["status_id"] = CompensationStatus.WAITING_FOR_CLARIFICATION.value
            invalid_records.append({
                "file_name": record["file_name"],
                "missing_fields": missing_fields
            })
        else:
            record["status_id"] = CompensationStatus.OPEN.value

    if invalid_records:
        clarification(user_email, invalid_records)

    return parsed_data  # ✅ Returns updated dictionary

def clarification(user_email, invalid_records):
    mail_body = generate_clarification_letter(invalid_records)
    send_clarification_letter(user_email, mail_body)


def generate_clarification_letter(invalid_records: List[Dict]) -> str:
    """
    Generates a single clarification letter summarizing all missing fields.

    Returns:
    - A formatted string containing the email request for missing information.
    - If no missing fields, returns `None`.
    """
    if not invalid_records:
        return None  # ✅ No clarification needed

    clarification_details = [
        f"- **File:** {record.get('file_name', 'Unknown File')}\n"
        f"  **Missing Fields:** {', '.join([field.replace('_', ' ').title() for field in record['missing_fields']])}\n"
        for record in invalid_records
    ]

    return (
        "Dear User,\n\n"
        "We received your benefit requests, but some required fields are missing. "
        "Please provide the missing details for the following documents:\n\n"
        + "\n".join(clarification_details) +
        "\n\nPlease reply with the required information so we can proceed with your request.\n\n"
        "Best regards,\nBenefits Processing Team"
    )


def convert_date_format(date_str):
    """
    Converts date from 'DD.MM.YYYY' to 'YYYY-MM-DD' for PostgreSQL.

    Args:
        date_str (str): Date in format 'DD.MM.YYYY'
    
    Returns:
        str: Date in format 'YYYY-MM-DD' or None if invalid.
    """
    if not date_str:
        return None  # ✅ Handle missing dates safely

    try:
        return datetime.strptime(date_str, "%d.%m.%Y").strftime("%Y-%m-%d")  # ✅ Convert format
    except ValueError:
        print(f"❌ Invalid date format: {date_str}")
        return None  # ✅ Skip invalid dates
