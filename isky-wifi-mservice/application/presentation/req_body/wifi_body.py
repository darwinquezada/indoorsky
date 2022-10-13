from pydantic import BaseModel, Field
from typing import Optional

class WifiFingerprintIdBody(BaseModel):
    fingerprint_id: str = Field(description="Fingerprint ID")

class WifiIdBody(BaseModel):
    wifi_id: str = Field(description="WiFi Fingerprint ID")
    