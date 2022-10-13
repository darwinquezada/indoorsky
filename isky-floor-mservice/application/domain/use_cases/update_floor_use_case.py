import json
from application.domain.repository.floor_repository import FloorRepository
from dependency_injector.wiring import inject

class UpdateFloorUseCase:
    @inject
    def __init__(self, floor_repository: FloorRepository) -> None:
        self.floor_repository = floor_repository
        
    def execute(self, floor_id: str, building_id: str, level: str, 
                is_public: bool, is_active: bool) -> dict:
        return self.floor_repository.update_floor_by_id(floor_id=floor_id, building_id=building_id,
                                                        level=level, is_public=is_public, is_active=is_active)