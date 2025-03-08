from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class CompensationRequest(BaseModel):
    id: UUID
    requestDate: str
    email: str
    fullName: Optional[str] = None
    requestStatus: str
    benefitProgram: Optional[str] = None
    location: Optional[str] = None
    totalUsed: float  # Converted from MONEY
