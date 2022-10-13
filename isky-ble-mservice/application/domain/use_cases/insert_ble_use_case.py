import json
from application.domain.repository.ble_repository import BleRepository
from dependency_injector.wiring import inject

class InsertbleUseCase:
    @inject
    def __init__(self, ble_repository: BleRepository) -> None:
        self.ble_repository = ble_repository
        
    def execute(self, data: json) -> dict:
        return self.ble_repository.insert_ble(data=data)