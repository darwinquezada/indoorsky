from pydantic import BaseModel, Field


class FingerprintIdBody(BaseModel):
    fingerprint_id: str = Field(description="Fingerprint ID")

class FingerprintEnvBody(BaseModel):
    env_id: str = Field(description="Fingerprint environment ID")
    
class FingerprintBuildingBody(BaseModel):
    building_id: str = Field(description="Fingerprint building ID")
    
class FingerprintFloorBody(BaseModel):
    floor_id: str = Field(description="Fingerprint floor ID")
    
class FingerprintPoiBody(BaseModel):
    poi_id: str = Field(description="Fingerprint POI ID")