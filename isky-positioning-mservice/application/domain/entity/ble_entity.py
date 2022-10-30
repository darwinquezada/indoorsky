from pydantic import BaseModel

class BleEntity(BaseModel):
    device_id: str
    name: str
    rssi: int    

    