from abc import ABC, abstractmethod
import json

class IFloorDatasource(ABC):
    
    @abstractmethod
    def insert_floor(self, data: json) -> dict:
        pass
    
    @abstractmethod
    def delete_floor(self, floor_id: str) -> dict:
        pass
    
    @abstractmethod
    def get_floor_by_id(self, floor_id: str) -> dict:
        pass
    
    @abstractmethod
    def get_floor_by_level(self, level: str) -> dict:
        pass
    
    @abstractmethod
    def update_floor_by_id(self, floor_id: str, building_id: str,
                           level: str, is_public: bool, is_active: bool) -> dict:
        pass