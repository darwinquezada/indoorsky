from pydantic import BaseModel
from typing import Optional

class PoiEntity(BaseModel):
    floor_id: str
    name: str
    description: Optional[str]
    image: Optional[str]
    latitude: float
    longitude: float
    altitude: float
    pos_x: float
    pos_y: float
    pos_z: float
    is_active: bool
    is_public: bool