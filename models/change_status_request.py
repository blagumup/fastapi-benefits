from pydantic import BaseModel

class ChangeStatusRequest(BaseModel):
    request_id: str
    status_id: str