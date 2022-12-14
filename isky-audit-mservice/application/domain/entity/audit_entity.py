from pydantic import BaseModel
from typing import Optional

class AuditEntity(BaseModel):
    """
    Audit entity
    """
    user_id: str
    local_ip: str
    external_ip: str
    event: str
    description: str