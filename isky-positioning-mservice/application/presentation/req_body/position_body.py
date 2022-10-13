from pydantic import BaseModel, Field
from typing import List


class PositionBody(BaseModel):
    rss: str = Field(description='RSSI value')
    ssid: str = Field(description='SSID name')
    bssid: str = Field(description='BSSID name')

class ListPositionBody(BaseModel):
    technology: str = Field(description='Technology')
    name: List[PositionBody]
