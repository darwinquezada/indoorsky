import json
from application.domain.repository.ble_repository import BleRepository
from dependency_injector.wiring import inject

class DeleteBleByFingerprintIdUseCase:
    @inject
    def __init__(self, ble_repository: BleRepository) -> None:
        self.ble_repository = ble_repository
        
    def execute(self, fingerprint_id: str) -> dict:
        return self.ble_repository.delete_ble_by_fingerprint_id(fingerprint_id=fingerprint_id)