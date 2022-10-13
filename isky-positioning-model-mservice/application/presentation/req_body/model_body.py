import imp
from pydantic import BaseModel, Field
from typing import Optional

class ModelNameBody(BaseModel):
    name: str = Field(description="Model name")

class ModelIdBody(BaseModel):
    model_id: str = Field(description="Model ID")

class FloorBody(BaseModel):
    building_id: str = Field(description="Building ID")
    level: str = Field(level="Level")
    is_public: bool = Field(is_public="Is it public?")
    is_active: bool = Field(is_active="Is it active?")