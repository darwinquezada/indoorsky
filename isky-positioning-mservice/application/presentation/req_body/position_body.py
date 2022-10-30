from os import device_encoding
from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class ModelEnum(str, Enum):
    cnn_lstm = 'CNN-LSTM'
    cnn_elm = 'CNN-ELM'
    
class ModelTypeEnum(str, Enum):
    position = 'POSITIONING'
    building = 'BUILDING'
    floor = 'FLOOR'

class ModelIdBody(BaseModel):
    model_id: str = Field(description='Model ID')

class WiFiBody(BaseModel):
    rss: str = Field(description='RSSI value')
    ssid: str = Field(description='SSID name')
    bssid: str = Field(description='BSSID name')

class ListWifiBody(BaseModel):
    list_wifi: List[WiFiBody]

class BleBody(BaseModel):
    device_id: str = Field(description='Device ID')
    name: str = Field(description='Device name')
    rss: str = Field(description='RSS value')

class ListBleBody(BaseModel):
    list_ble: List[BleBody]
    
class ModelBody(BaseModel):
    model: ModelEnum
    model_type: ModelTypeEnum
    data_model_id: str
    pos_tech_id: str
    
class ModelTypeBody(BaseModel):
    model_type: ModelTypeEnum

class PathGetPostionBody(BaseModel):
    pos_tech_id: str
    model_type: ModelTypeEnum