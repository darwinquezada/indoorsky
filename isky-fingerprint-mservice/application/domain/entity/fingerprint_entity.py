from pydantic import BaseModel
from typing import List, Optional

class FingerprintEntity(BaseModel):
    id: str
    user_device: str
    os: str
    version: str
    env_id: Optional[str]
    building_id: Optional[str]
    floor_id: Optional[str]
    poi_id: str