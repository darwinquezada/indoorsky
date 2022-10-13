from pydantic import BaseModel

class BleEntity(BaseModel):
    id: str
    name: str
    rssi: int    

    