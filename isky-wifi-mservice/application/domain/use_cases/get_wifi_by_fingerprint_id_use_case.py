import json
from application.domain.repository.wifi_repository import WifiRepository
from dependency_injector.wiring import inject

class GetWifiByFingerprintIdUseCase:
    @inject
    def __init__(self, wifi_repository: WifiRepository) -> None:
        self.wifi_repository = wifi_repository
        
    def execute(self, fingerprint_id: str) -> dict:
        return self.wifi_repository.get_wifi_by_fingerprint_id(fingerprint_id=fingerprint_id)