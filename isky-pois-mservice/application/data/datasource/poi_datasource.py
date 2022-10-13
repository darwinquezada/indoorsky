from abc import ABC, abstractmethod
import json

class IPoiDatasource(ABC):
    
    @abstractmethod
    def verify_db(self) -> dict:
        pass
    
    @abstractmethod
    def verify_table(self) -> dict:
        pass
    
    @abstractmethod
    def insert_poi(self, data: json) -> dict:
        pass
    
    @abstractmethod
    def delete_poi(self, poi_id: str) -> dict:
        pass
    
    @abstractmethod
    def get_poi_by_id(self, poi_id: str) -> dict:
        pass
    
    @abstractmethod
    def get_poi_by_name(self, name: str) -> dict:
        pass
    
    @abstractmethod
    def update_poi_by_id(self, poi_id: str, floor_id: str, name: str, description: str, image: str,
                         latitude: float, longitude: float, altitude: float, pos_x: float,
                         pos_y: float, pos_z: float, is_active: bool, is_public: bool) -> dict:
        pass