from pydantic import BaseModel, Field
from typing import Optional

class BleFingerprintIdBody(BaseModel):
    fingerprint_id: str = Field(description="Fingerprint ID")

class BleIdBody(BaseModel):
    ble_id: str = Field(description="Ble Fingerprint ID")
    