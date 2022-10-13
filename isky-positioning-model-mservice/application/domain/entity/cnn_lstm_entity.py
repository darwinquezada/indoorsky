from pydantic import BaseModel
from enum import Enum

class LossEnum(str, Enum):
    mse = 'mse'
    
class OptimizerEnum(str, Enum):
    adam = 'Adam'
    adamax = 'Adamax'
    adadelta = 'Adadelta'
    adagrad = 'Adagrad'
    ftrl = 'Ftrl'
    nadam = 'Nadam'
    rmsprop = 'RMSprop'
    
class MetricEnum(str, Enum):
    manhattan= 'manhattan'
    euclidean= 'euclidean'
    
class TestEntity(BaseModel):
    test_accuracy: bool = False
    percent_test: int

class GeneralModelEntity(BaseModel):
    lr: float
    epochs: int
    batch_size: int
    loss: LossEnum
    optimizer: OptimizerEnum = 'Adam'

class CnnLstmEntity(BaseModel):
    name: str
    dataset_id: str
    floor: GeneralModelEntity
    building: GeneralModelEntity
    position: GeneralModelEntity
    test : TestEntity
    is_active: bool