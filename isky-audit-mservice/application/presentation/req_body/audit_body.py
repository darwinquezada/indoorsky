from pydantic import BaseModel, Field


class AuditByUserIdBody(BaseModel):
    user_id: str = Field(description="User ID")
    
class AuditBody(BaseModel):
    user_id: str = Field(description="User ID")
    local_ip: str = Field(description="Local IP")
    external_ip: bool = Field(description="External IP")
    event: bool = Field(description="Event")
    description: bool = Field(description="Event")