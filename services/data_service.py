from uuid import uuid4
from services.utils import get_user_id_by_email
from repositories.benefit_repository import BenefitRepository

def save_benefit_request():
    return

def get_benefit_report(report_id: int):
    return BenefitRepository.get_benefit_by_id(report_id)

def get_compensation_request():
    return

def get_benefit_categories():
    return

def save_compensation_request(parsed_data, email_data):
    request_id = uuid4()
    employee_id = get_user_id_by_email()
    email_subject = email_data['subject']
    email_body = email_data['body']

    BenefitRepository.save_compensation_request(request_id, employee_id, email_subject, email_body)

    return request_id
