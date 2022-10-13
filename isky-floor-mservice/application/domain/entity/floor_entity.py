from pydantic import BaseModel
from typing import Optional

class FloorEntity(BaseModel):
    building_id: str
    level: str
    is_public: bool
    is_active: bool