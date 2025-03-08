from pydantic import BaseModel
from typing import Optional

class BenefitCategoryDbModel(BaseModel):
    categoryId: int
    categoryName: str
    description: Optional[str] = None
    coverAmount: float
    coverSize: float
