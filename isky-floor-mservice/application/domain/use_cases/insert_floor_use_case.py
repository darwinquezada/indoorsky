import json
from application.domain.repository.floor_repository import FloorRepository
from dependency_injector.wiring import inject

class InsertFloorUseCase:
    @inject
    def __init__(self, floor_repository: FloorRepository) -> None:
        self.floor_repository = floor_repository
        
    def execute(self, data: json)->dict:
        return self.floor_repository.insert_floor(data=data)