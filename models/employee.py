from pydantic import BaseModel

class Employee(BaseModel):
    employee_id: str
    employee_email: str