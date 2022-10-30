from abc import ABC, abstractmethod
import json

class PositioningRepository(ABC):
    
    @abstractmethod
    def get_position(self, pos_tech_id:str, model_type:str, data: json) -> dict:
        pass
    
    @abstractmethod
    def set_models(self, model: json) -> dict:
        pass
    
    @abstractmethod
    def delete_set_model(self, set_model_id: str) -> dict:
        pass
    
    @abstractmethod
    def update_set_model(self, set_model_id: str, model: json) -> dict:
        pass
    
    @abstractmethod
    def get_set_model_by_model_type(self, model_type: str) -> dict:
        pass