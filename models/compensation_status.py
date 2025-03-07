from enum import Enum

class CompensationStatus(Enum):
    OPEN = 1
    APPROVED = 2
    WAITING_FOR_CLARIFICATION = 3
    DECLINED = 4
    CANCELLED = 5
    EXCEEDED_LIMIT = 6
    PROCESSED = 7
