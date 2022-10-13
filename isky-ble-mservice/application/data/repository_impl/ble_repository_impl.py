import json
from application.domain.repository.ble_repository import BleRepository
from application.data.datasource.ble_datasource import IBleDatasource

class BleRepositoryImpl(BleRepository):
    def __init__(self, ble_datasource: IBleDatasource) -> None:
        self.ble_datasource = ble_datasource
        
    def get_ble_by_id(self, ble_id: str) -> dict:
        return self.ble_datasource.get_ble_by_id(ble_id)
    
    def get_ble_by_fingerprint_id(self, fingerprint_id: str) -> dict:
        return self.ble_datasource.get_ble_by_fingerprint_id(fingerprint_id)
    
    def insert_ble(self, data: json) -> dict:
        return self.ble_datasource.insert_ble(data)
    
    def delete_ble_by_id(self, ble_id: str) -> dict:
        return self.ble_datasource.delete_ble_by_id(ble_id)
    
    def delete_ble_by_fingerprint_id(self, fingerprint_id: str) -> dict:
        return self.ble_datasource.delete_ble_by_fingerprint_id(fingerprint_id)
        