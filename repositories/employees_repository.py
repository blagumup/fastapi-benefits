from models.employee import Employee
from repositories.database import db

#TODO need to use convert model methods in prod version
class EmployeeRepository:
    @staticmethod
    def get_all_employees():
        """Retrieve all employees."""
        result = db.fetch('fn_employees_get_all')

        if not result:
            return []

        return [Employee(employee_id=row[0], employee_email=row[1]) for row in result]

    @staticmethod
    def get_employee_by_id(employee_id):
        """Retrieve an employee by ID."""
        result = db.fetch('fn_employee_get_by_id', employee_id)

        if not result or len(result) == 0:
            return None

        row = result[0]
        return Employee(employee_id=row[0], employee_email=row[1])
