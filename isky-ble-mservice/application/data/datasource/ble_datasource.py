from abc import ABC, abstractmethod
import json

class IBleDatasource(ABC):
    
    @abstractmethod
    def verify_db(self) -> dict:
        pass
    
    @abstractmethod
    def verify_table(self) -> dict:
        pass
    
    @abstractmethod
    def insert_ble(self, data: json) -> dict:
        pass
    
    @abstractmethod
    def get_ble_by_id(self, ble_id: str) -> dict:
        pass
    
    @abstractmethod
    def get_ble_by_fingerprint_id(self, fingerprint_id: str) -> dict:
        pass
    
    @abstractmethod
    def delete_ble_by_id(self, ble_id: str) -> dict:
        pass
    
    @abstractmethod
    def delete_ble_by_fingerprint_id(self, fingerprint_id: str) -> dict:
        pass
    