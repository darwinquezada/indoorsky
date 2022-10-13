from pydantic import BaseModel, Field


class CleansingIdBody(BaseModel):
    cleansing_id: str = Field(description="Data cleansing ID")
    
class CleansingNameBody(BaseModel):
    name: str = Field(description="Data cleansing name")
    
class CleansingEnvIdBody(BaseModel):
    env_id: str = Field(description="Environment ID")