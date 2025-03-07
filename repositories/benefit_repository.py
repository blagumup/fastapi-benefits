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
        # return db.fetch('fn_user_benefit_categories_get', '31f66b01-d59b-4a7e-8ea7-5df283aa55fb')
        return db.fetch('fn_benefit_categories_get_all')

    @staticmethod
    def get_benefit_by_id(benefit_id):
        """Retrieve a benefit by ID."""
        query = "SELECT * FROM benefits WHERE id = %s;"
        return db.fetch(query, benefit_id)
