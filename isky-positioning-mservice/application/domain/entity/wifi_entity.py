from pydantic import BaseModel

class WifiEntity(BaseModel):
    ssid: str
    bssid: str
    rssi: int