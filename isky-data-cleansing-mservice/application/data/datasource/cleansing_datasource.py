from abc import ABC, abstractmethod
import json

class IDataCleansingDatasource(ABC):
    
    @abstractmethod
    def clean_dataset(self, data: json) -> dict:
        pass
    
    @abstractmethod
    def delete_cleansed_dataset(self, clean_id: str) -> dict:
        pass
    
    @abstractmethod
    def get_cleansed_dataset_by_id(self, clean_id: str) -> dict:
        pass
    
    @abstractmethod
    def get_cleansed_dataset_by_name(self, name: str) -> dict:
        pass
    
    @abstractmethod
    def get_cleansed_dataset_by_env(self, env_id: str) -> dict:
        pass
    