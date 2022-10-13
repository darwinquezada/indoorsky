from pydantic import BaseModel
from typing import Optional

class WifiEntity(BaseModel):
    fingerprint_id: str
    ssid: str
    bssid: str
    rssi: str
    