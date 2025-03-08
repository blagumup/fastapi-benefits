from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class CompensationRequestRecord(BaseModel):
    requestId: UUID
    recordId: UUID
    transactionDate: str
    categoryId: int
    category: str
    statusId: int
    fullName: Optional[str] = None
    recipient: Optional[str] = None
    recipeAmountLocal: float
    recipeCurrency: str
    recipeAmountUsd: float
    recipeStatus: str
    attachmentId: Optional[UUID] = None
    fileName: Optional[str] = None
    filePath: Optional[str] = None
