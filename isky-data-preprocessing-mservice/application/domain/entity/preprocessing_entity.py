from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class DataRepresentationEnum(str, Enum):
    positive = 'positive'
    powed = 'powed'
    exponential = 'exponential'
    none = 'none'
    
class NormalizationEnum(str, Enum):
    min_max_scaler = 'minmax' 
    standard_scaler = 'stardard'
    robust_scaler = 'robust'
    normalizer = 'normalizer'
    none = 'none'
    
class PreprocessingEntity(BaseModel):
    name: str
    env_id: str
    building_id: Optional[str]
    floor_id: Optional[str]
    data_representation: Optional[DataRepresentationEnum] = Field(description="Type of data representation.")
    x_normalization : Optional[NormalizationEnum] = Field(description="Data normalization.")
    y_normalization : Optional[NormalizationEnum] = Field(description="Latitude, longitude and altitude normalization.")
    pos_tech_id: str = Field(description="Positioning technology ID.")
    date_start: Optional[float] = Field(description="Unix timestamp format with milliseconds.")
    date_end: Optional[float] = Field(description="Unix timestamp format with milliseconds.")
    non_dected_value: int
    is_active: bool