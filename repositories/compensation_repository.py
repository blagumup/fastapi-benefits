from repositories.database import db

class CompensationRepository:
    @staticmethod
    def get_all_compensation_requests():
        """Retrieve all compensation records."""
        return db.fetch('fn_compensation_requests_get_all')
    
    @staticmethod
    def save_compensation_request(request_id, employee_id, email_subject, email_body, parsed_data):
        db.execute("fn_upload_request_data", request_id, employee_id, email_subject, email_body, parsed_data)
