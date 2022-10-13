from pydantic import BaseModel
from typing import Optional

class BleEntity(BaseModel):
    fingerprint_id: str
    device_id: str
    name: str
    rssi: str
    