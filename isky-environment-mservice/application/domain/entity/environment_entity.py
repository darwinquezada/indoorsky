from pydantic import BaseModel
from typing import List, Optional

class EnvironmentEntity(BaseModel):
    name: str
    address: Optional[str]
    num_buildings: int
    is_public: bool
    is_active: bool