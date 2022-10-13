import json
from application.domain.repository.building_repository import BuildingRepository
from dependency_injector.wiring import inject

class GetBuildingByIdUseCase:
    @inject
    def __init__(self, building_repository: BuildingRepository) -> None:
        self.building_repository = building_repository
        
    def execute(self, building_id: str) -> dict:
        return self.building_repository.get_building_by_id(building_id=building_id)