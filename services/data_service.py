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