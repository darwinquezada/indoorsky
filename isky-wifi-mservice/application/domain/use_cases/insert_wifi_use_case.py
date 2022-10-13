import json
from application.domain.repository.wifi_repository import WifiRepository
from dependency_injector.wiring import inject

class InsertWifiUseCase:
    @inject
    def __init__(self, wifi_repository: WifiRepository) -> None:
        self.wifi_repository = wifi_repository
        
    def execute(self, data: json) -> dict:
        return self.wifi_repository.insert_wifi(data=data)