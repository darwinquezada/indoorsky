from pydantic import BaseModel, Field


class PosTechIdBody(BaseModel):
    pos_tech_id: str = Field(description="Positioning Technology ID")
    
class PosTechNameBody(BaseModel):
    name: str = Field(description="Positioning Technology Name")
