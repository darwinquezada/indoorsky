from pydantic import BaseModel
from typing import Optional

class BuildingEntity(BaseModel):
    env_id: str
    name: str
    num_floors: int
    description: Optional[str]
    latitude: float
    longitude: float
    altitude: Optional[float]
    is_public: bool
    is_active: bool