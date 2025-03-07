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
    request_id = uuid4()
    employee_id = get_user_id_by_email()
    email_subject = email_data['subject']
    email_body = email_data['body']

    BenefitRepository.save_compensation_request(request_id, employee_id, email_subject, email_body)

    return request_id