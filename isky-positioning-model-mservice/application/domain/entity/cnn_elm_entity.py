from pydantic import BaseModel, Field
from enum import Enum

class ActivationFunctionsEnum(str, Enum):
    tan = 'tan'
    sigmoid = 'sigmoid'
    tanh = 'tanh'
    tansig = 'tansig'
    linsat = 'linsat'
    relu = 'relu'
    absolute = 'abs'
    sine = 'sine'
    cosine = 'cosine'
    linear = 'linear'
    
class DataFormatEnum(str, Enum):
    channel_last = 'channels_last'
    channel_first = 'channels_first'
    
class PaddingEnum(str, Enum):
    same = 'same'
    valid = 'valid'
    
class WeightInitializatioEnum(str, Enum):
    orthogonal = 'orthogonal'
    random = 'random'
    
class MetricEnum(str, Enum):
    manhattan= 'manhattan'
    euclidean= 'euclidean'
    
class TestEntity(BaseModel):
    test_accuracy: bool = False
    percent_test: int
    k : int = 1
    distance_metric: MetricEnum = 'manhattan'

class ElmEntity(BaseModel):
    act_funct: ActivationFunctionsEnum = Field(description='Activation Function')
    c : float = Field(description='Regurization term')
    hidden_neurons: int = Field(description="Number of hidden neurons")
    weight_intialization : WeightInitializatioEnum = 'random' 
    weight_initializatio_bits: int = 2
    output_weits_bits: int = 8
    
class CnnEntity(BaseModel):
    padding: PaddingEnum = Field(description='CNN Padding')
    strides: int = 1 
    act_funct: ActivationFunctionsEnum = 'abs'
    data_format: DataFormatEnum = 'channels_last'
    kernel_size: int = 1
    filter: int = 1

class CnnElmEntity(BaseModel):
    name: str
    dataset_id: str
    cnn: CnnEntity
    elm: ElmEntity
    test: TestEntity
    is_active: bool