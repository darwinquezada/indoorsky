from pydantic import BaseModel, Field


class EnvironmentBody(BaseModel):
    data: dict = Field(...,description="Environment Information")
    
class EnvironmentId(BaseModel):
    env_id: str = Field(...,description="Environment ID")
    
class EnvironmentName(BaseModel):
    name: str = Field(...,description="Environment name")