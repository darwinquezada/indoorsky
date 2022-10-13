from abc import ABC, abstractmethod
import json

class BuildingRepository(ABC):
    @abstractmethod
    def insert_building(self, data: json) -> dict:
        pass
    
    @abstractmethod
    def delete_building(self, building_id: str) -> dict:
        pass
    
    @abstractmethod
    def get_building_by_id(self, building_id: str) -> dict:
        pass
    
    @abstractmethod
    def get_building_by_name(self, name: str) -> dict:
        pass
    
    @abstractmethod
    def update_building_by_id(self, building_id: str, env_id: str, 
                              name: str, num_floors: int, description: str,
                              latitude: float, longitude: float, altitude: float,
                              is_public: bool, is_active: bool) -> dict:
        pass