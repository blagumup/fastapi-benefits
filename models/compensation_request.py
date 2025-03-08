from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class CompensationRequest(BaseModel):
    id: UUID
    requestDate: str  # Converted from TIMESTAMP
    email: str
    fullName: Optional[str] = None  # Nullable
    requestStatus: str
    benefitProgram: Optional[str] = None  # Nullable
    location: Optional[str] = None  # Nullable
    totalUsed: float  # Converted from MONEY
