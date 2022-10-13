from application.domain.repository.floor_repository import FloorRepository
from dependency_injector.wiring import inject

class GetFloorByLevelUseCase:
    @inject
    def __init__(self, floor_repository: FloorRepository) -> None:
        self.floor_repository = floor_repository
        
    def execute(self, level: str) -> dict:
        return self.floor_repository.get_floor_by_level(level=level)