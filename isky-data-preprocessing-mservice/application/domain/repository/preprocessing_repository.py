from abc import ABC, abstractmethod
import json

class PreprocessingRepository(ABC):
    @abstractmethod
    def preprocess_data(self, data: json) -> dict:
        pass
    
    @abstractmethod
    def get_data_preprocessed_by_id(self, conf_prepro_id: str) -> dict:
        pass
    
    @abstractmethod
    def delete_data_preprocessed_by_id(self, conf_prepro_id: str) -> dict:
        pass
    
    @abstractmethod
    def get_data_preprocessed_by_env(self, env_id:str) -> dict:
        pass