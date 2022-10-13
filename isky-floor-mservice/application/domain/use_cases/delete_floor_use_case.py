from application.domain.repository.floor_repository import FloorRepository
from dependency_injector.wiring import inject

class DeleteFloorUseCase:
    @inject
    def __init__(self, floor_repository: FloorRepository) -> None:
        self.floor_repository = floor_repository
        
    def execute(self, floor_id: str) -> dict:
        return self.floor_repository.delete_floor(floor_id=floor_id)