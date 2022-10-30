from pydantic import BaseModel, Field


class AuditByUserIdBody(BaseModel):
    user_id: str = Field(description="User ID")
    
class AuditBody(BaseModel):
    user_id: str = Field(description="User ID")
    local_ip: str = Field(description="Local IP")
    external_ip: str = Field(description="External IP")
    event: str = Field(description="Event")
    description: str = Field(description="Event")