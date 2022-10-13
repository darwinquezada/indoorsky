from pydantic import BaseModel, Field


class PreprocessingIdBody(BaseModel):
    preprocessing_id: str = Field(description="Preprocessing ID")
    
class PreprocessingEnvIdBody(BaseModel):
    env_id: str = Field(description="Environment ID")
    
