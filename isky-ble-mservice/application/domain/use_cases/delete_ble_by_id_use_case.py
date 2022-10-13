import json
from application.domain.repository.ble_repository import BleRepository
from dependency_injector.wiring import inject

class DeleteBleByIdUseCase:
    @inject
    def __init__(self, ble_repository: BleRepository) -> None:
        self.ble_repository = ble_repository
        
    def execute(self, ble_id: str) -> dict:
        return self.ble_repository.delete_ble_by_id(ble_id=ble_id)