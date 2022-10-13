import imp
from pydantic import BaseModel, Field
from typing import Optional

class BuildingNameBody(BaseModel):
    name: str = Field(description="Building name")

class BuildingIdBody(BaseModel):
    building_id: str = Field(description="Building ID")
    
class BuildingBody(BaseModel):
    env_id: str = Field(description="environment ID")
    name: str = Field(description="Building name")
    num_floors: int = Field(description="Number of floors")
    description: Optional[str] = Field(description="Building description")
    latitude: float = Field(description="Latitude")
    longitude: float = Field(description="Longitude")
    altitude: Optional[float] = Field(description="altitude")
    is_public: bool = Field(description="Is it public?")
    is_active: bool = Field(description="Is it active")