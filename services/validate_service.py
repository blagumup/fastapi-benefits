from typing import List, Dict
from models.compensation_status import CompensationStatus
from services.mail_service import send_clarification_letter

REQUIRED_FIELDS = ["file_name", "category", "username", "document_number", "document_date", "document_sum", "document_currency", "account_number"]

def validate_and_set_status(user_email, parsed_data: List[Dict]) -> List[Dict]:
    """
    Validates parsed OCR data, updates each item with `status_id`, and returns the updated list.
    
    Status IDs:
    - `1`: Data is complete ✅
    - `2`: Data is missing required fields and needs clarification ❌
    
    Returns:
    - Updated list with `status_id` added to each item.
    """
    invalid_records = []

    for record in parsed_data:
        missing_fields = [field for field in REQUIRED_FIELDS if not record.get(field)]
        
        # Assign status based on missing fields
        if missing_fields:
            record["status_id"] = CompensationStatus.WAITING_FOR_CLARIFICATION
            invalid_records.append({
                "file_name": record["file_name"],
                "missing_fields": missing_fields
            })
        else:
            record["status_id"] = CompensationStatus.OPEN

    if invalid_records:
        clarification(invalid_records)

    return parsed_data

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

