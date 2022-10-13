from pydantic import BaseModel
from typing import List, Optional
from typing import Optional
from enum import Enum

class Metric(str, Enum):
    manhattan= 'manhattan'
    euclidean= 'euclidean'
    
class TestEntity(BaseModel):
    test_accuracy: bool = False
    percent_test: int
    k : int = 1
    distance_metric: Metric = 'manhattan'

class CleansingEntity(BaseModel):
    name: str
    threshold: int = 1
    dataset_id: str
    test: Optional[TestEntity]
    