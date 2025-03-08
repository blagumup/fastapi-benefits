from models.benefit_category_db_model import BenefitCategoryDbModel
from repositories.database import db

class BenefitRepository:
    @staticmethod
    def get_all_benefits():
        """Retrieve all benefits."""
        result = db.fetch('fn_benefit_categories_get_all')

        if not result:
            return []  # Return an empty list instead of None

        # Map database response to BenefitCategory model
        formatted_results = [
            BenefitCategoryDbModel(
                categoryId=row[0],  # category_id
                categoryName=row[1],  # category_name
                description=row[2],  # description
                coverAmount=float(row[3].replace("$", "").replace(",", "")) if row[3] is not None else 0.0,  # ✅ Convert MONEY to float
                coverSize=float(row[4])  # NUMERIC(3,2)
            ).model_dump()  # ✅ Use model_dump() for Pydantic v2
            for row in result
        ]

        return formatted_results    
