from pydantic import BaseModel

class WifiEntity(BaseModel):
    ssid: str
    bssid: str
    rssi: int
    
class BleEntity(BaseModel):
    id: str
    name: str
    rssi: int    

    