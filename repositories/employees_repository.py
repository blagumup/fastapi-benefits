from repositories.database import db

class EmployeeRepository:
    @staticmethod
    def get_all_employees():
        """Retrieve all employees."""
        return db.fetch('fn_employees_get_all')

    @staticmethod
    def get_employee_by_id(employee_id):
        """Retrieve an employee by ID."""
        return db.fetch('fn_employee_get_by_id', employee_id)
