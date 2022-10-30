from abc import ABC, abstractmethod
import json

class IWifiDatasource(ABC):
    
    @abstractmethod
    def insert_wifi(self, data: json) -> dict:
        pass
    
    @abstractmethod
    def get_wifi_by_id(self, wifi_id: str) -> dict:
        pass
    
    @abstractmethod
    def get_wifi_by_fingerprint_id(self, fingerprint_id: str) -> dict:
        pass
    
    @abstractmethod
    def delete_wifi_by_id(self, wifi_id: str) -> dict:
        pass
    
    @abstractmethod
    def delete_wifi_by_fingerprint_id(self, fingerprint_id: str) -> dict:
        pass
    