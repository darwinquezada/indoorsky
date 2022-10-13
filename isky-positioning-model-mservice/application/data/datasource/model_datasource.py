from abc import ABC, abstractmethod
import json

class IModelDatasource(ABC):
    
    @abstractmethod
    def train_model(self, data: json, model: str) -> dict:
        pass
    
    @abstractmethod
    def delete_model_by_id(self, model_id: str) -> dict:
        pass
    
    @abstractmethod
    def get_model_by_id(self, model_id: str) -> dict:
        pass
    
    @abstractmethod
    def get_model_by_name(self, name: str) -> dict:
        pass
    