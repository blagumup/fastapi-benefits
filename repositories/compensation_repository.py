from models.compensation_request import CompensationRequest
from repositories.database import db

#TODO need to use convert model methods in prod version
class CompensationRepository:
    @staticmethod
    def get_all_compensation_requests():
        """Retrieve all compensation records."""
        result = db.fetch('fn_compensation_requests_get_all')

        if not result:
            return []

        formatted_results = [
            CompensationRequest(
                id=row[0],  # request_id (UUID)
                requestDate=row[4].isoformat(),  # Convert TIMESTAMP to string
                email=row[3],  # email
                fullName=row[2],  # full_name
                requestStatus=row[7],  # request_status
                benefitProgram=row[8],  # benefit_program
                location=row[9],  # location
                totalUsed=float(row[11].replace("$", "").replace(",", "")) if row[11] is not None else 0.0  # MONEY conversion
            ).model_dump()
            for row in result
        ]

        return formatted_results
    
    @staticmethod
    def save_compensation_request(request_id, employee_id, email_subject, email_body, parsed_data):
        db.execute("fn_upload_request_data", request_id, employee_id, email_subject, email_body, parsed_data)
