from abc import ABC, abstractmethod
import json

class FingerprintRepository(ABC):
    
    @abstractmethod
    def insert_fingerprint(self, data: json) -> dict:
        pass
    
    @abstractmethod
    def get_fingerprint_by_id(self, fp_id: str) -> dict:
        pass
    
    @abstractmethod
    def get_fingerprint_by_field(self, field: str, value: str) -> dict:
        pass
   
    @abstractmethod
    def delete_fingerprint_by_id(self, fp_id: str) -> dict:
        pass
    
    @abstractmethod
    def delete_fingerprint_by_field(self, field: str, value: str) -> dict:
        pass
    
    