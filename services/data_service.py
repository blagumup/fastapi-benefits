import base64
import json
import os
from uuid import uuid4
from services.utils import get_user_id_by_email
from repositories.benefit_repository import BenefitRepository
from repositories.employees_repository import EmployeeRepository
from repositories.compensation_repository import CompensationRepository

def save_benefit_request():
    return

def get_benefit_report(report_id: int):
    return BenefitRepository.get_benefit_by_id(report_id)

def get_compensation_request():
    return

def get_compensation_requests():
    return CompensationRepository.get_all_compensation_requests()

def get_benefit_categories():
    return BenefitRepository.get_all_benefits()

def get_employees():
    return EmployeeRepository.get_all_employees()

def get_employee(employee_id: str):
    return EmployeeRepository.get_employee_by_id(employee_id)

def save_compensation_request(parsed_data, email_data):
    request_id = str(uuid4())
    employee_id = get_user_id_by_email()
    email_subject = email_data['subject']
    email_body = email_data['body']
    parsed_data_str = json.dumps(parsed_data, ensure_ascii=False)

    print(f"parsed_data_str: {parsed_data_str}")

    BenefitRepository.save_compensation_request(request_id, employee_id, email_subject, email_body, parsed_data_str)

    save_attachments_locally(request_id, email_data["attachments"])

    return request_id

def save_attachments_locally(request_id, attachments):
    """
    Saves email attachments to `attachments/{request_id}/` directory.

    Args:
        request_id (UUID): Unique ID for the compensation request.
        attachments (list[dict]): List of attachments with 'filename' and 'content'.
    """
    request_folder = os.path.join("attachments", str(request_id))  # noqa: F821
    os.makedirs(request_folder, exist_ok=True)  # ✅ Ensure directory exists

    for attachment in attachments:
        file_path = os.path.join(request_folder, attachment["filename"])
        file_content = base64.b64decode(attachment["content"])  # Decode Base64

        # ✅ Save file
        with open(file_path, "wb") as file:
            file.write(file_content)

        print(f"✅ Saved attachment: {file_path}")