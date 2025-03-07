from repositories.database import db

class CompensationRepository:
    @staticmethod
    def get_all_compensation_requests():
        """Retrieve all compensation records."""
        return db.fetch('fn_compensation_requests_get_all')
