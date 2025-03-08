from models.employee import Employee
from repositories.database import db

class EmployeeRepository:
    @staticmethod
    def get_all_employees():
        """Retrieve all employees."""
        return db.fetch('fn_employees_get_all')

    @staticmethod
    def get_employee_by_id(employee_id):
        """Retrieve an employee by ID."""
        result = db.fetch('fn_employee_get_by_id', employee_id)

        if not result or len(result) == 0:
            return None  # ✅ Return None if no employee found

        # ✅ Convert DB row to Employee model
        row = result[0]
        return Employee(employee_id=row[0], employee_email=row[1])
