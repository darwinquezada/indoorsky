from pydantic import BaseModel, Field


class FloorLevelBody(BaseModel):
    level: str = Field(description="Floor Level")

class FloorIdBody(BaseModel):
    floor_id: str = Field(description="Floor ID")
    
class FloorBody(BaseModel):
    building_id: str = Field(description="Building ID")
    level: str = Field(level="Level")
    is_public: bool = Field(is_public="Is it public?")
    is_active: bool = Field(is_active="Is it active?")