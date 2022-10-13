import json
from application.domain.repository.building_repository import BuildingRepository
from dependency_injector.wiring import inject

class GetBuildingByNameUseCase:
    @inject
    def __init__(self, building_repository: BuildingRepository) -> None:
        self.building_repository = building_repository
        
    def execute(self, name: str) -> dict:
        return self.building_repository.get_building_by_name(name=name)