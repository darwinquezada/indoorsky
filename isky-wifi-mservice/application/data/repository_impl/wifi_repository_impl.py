import json
from application.domain.repository.wifi_repository import WifiRepository
from application.data.datasource.wifi_datasource import IWifiDatasource

class WifiRepositoryImpl(WifiRepository):
    def __init__(self, wifi_datasource: IWifiDatasource) -> None:
        self.wifi_datasource = wifi_datasource
        
    def get_wifi_by_id(self, wifi_id: str) -> dict:
        return self.wifi_datasource.get_wifi_by_id(wifi_id)
    
    def get_wifi_by_fingerprint_id(self, fingerprint_id: str) -> dict:
        return self.wifi_datasource.get_wifi_by_fingerprint_id(fingerprint_id)
    
    def insert_wifi(self, data: json) -> dict:
        return self.wifi_datasource.insert_wifi(data)
    
    def delete_wifi_by_id(self, wifi_id: str) -> dict:
        return self.wifi_datasource.delete_wifi_by_id(wifi_id)
    
    def delete_wifi_by_fingerprint_id(self, fingerprint_id: str) -> dict:
        return self.wifi_datasource.delete_wifi_by_fingerprint_id(fingerprint_id)
        