from models.compensation_request import CompensationRequest
from models.compensation_request_record import CompensationRequestRecord
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

    @staticmethod
    def update_record_status(record_id: str, status_id):
        db.execute("fn_request_record_update_by_id", record_id, status_id)

    @staticmethod
    def get_compensation_request_by_id(request_id: str):
        """Retrieve a compensation request record by ID."""
        result = db.fetch('fn_request_records_get_by_id', request_id)

        if not result:
            return None  # Return None if no record is found

        # Assuming only one record is returned, take the first one
        row = result[0]

        # Map database response to CompensationRequestRecord model
        formatted_result = CompensationRequestRecord(
            requestId=row[0],  # request_id (UUID)
            recordId=row[1],  # record_id (UUID)
            transactionDate=row[2].isoformat() if row[2] is not None else "2000-01-01T00:00:00",  # ✅ Mock date if NULL (for POC)
            categoryId=row[3],  # category_id
            category=row[4],  # category_name
            statusId=row[5],  # status_id
            fullName=row[6],  # full_name
            recipient=row[7],  # recipient
            recipeAmountLocal=float(row[8].replace("$", "").replace(",", "")) if row[8] is not None else 0.0,  # ✅ Convert MONEY to float
            recipeCurrency=row[9],  # recipe_currency
            recipeAmountUsd=float(row[10].replace("$", "").replace(",", "")) if row[10] is not None else 0.0,  # ✅ Convert MONEY to float
            recipeStatus=row[11],  # status_name
            attachmentId=row[12],  # attachment_id (UUID, nullable)
            fileName=row[13],  # file_name (nullable)
            filePath=row[14]  # file_path (nullable)
        ).model_dump()

        return formatted_result
