from abc import ABC, abstractmethod
import json

class IPosTechDatasource(ABC):
    
    @abstractmethod
    def verify_db(self) -> dict:
        pass
    
    @abstractmethod
    def verify_table(self) -> dict:
        pass
    
    @abstractmethod
    def insert_pos_tech(self, data: json)->dict:
        pass
    
    @abstractmethod
    def get_pos_tech_by_id(self, pos_tech_id: str)->dict:
        pass
    
    @abstractmethod
    def get_pos_tech_by_name(self, name: str)->dict:
        pass
    
    @abstractmethod
    def delete_pos_tech_by_id(self, pos_tech_id: str)->dict:
        pass
    
    @abstractmethod
    def update_pos_tech_by_id(self, pos_tech_id: str, data: json)->dict:
        pass
    
    
    