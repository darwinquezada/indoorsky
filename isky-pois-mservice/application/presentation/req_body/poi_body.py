from pydantic import BaseModel, Field

class PoiNameBody(BaseModel):
    name: str = Field(description="User name")

class PoiIdBody(BaseModel):
    poi_id: str = Field(description="User ID")