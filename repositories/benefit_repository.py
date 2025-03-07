from repositories.database import db

class BenefitRepository:
    @staticmethod
    def save_benefit(username, email, amount, date, transaction_id, category, description):
        """Insert a new benefit request into the database."""
        query = """
        INSERT INTO benefits (username, email, amount, date, transaction_id, category, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        """
        db.execute(query, username, email, amount, date, transaction_id, category, description)

    @staticmethod
    def get_all_benefits():
        """Retrieve all benefits."""
        query = "SELECT * FROM benefits;"
        return db.fetch(query)

    @staticmethod
    def get_benefit_by_id(benefit_id):
        """Retrieve a benefit by ID."""
        # query = "SELECT * FROM benefits WHERE id = %s;"
        return db.fetch("procedure_name", benefit_id)
    
    @staticmethod
    def save_compensation_request(request_id, employee_id, email_subject, email_body):
        db.execute("procedure_name", request_id, employee_id, email_subject, email_body)
