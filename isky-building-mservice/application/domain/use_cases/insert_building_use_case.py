import json
from application.domain.repository.building_repository import BuildingRepository
from dependency_injector.wiring import inject

class InsertBuildingUseCase:
    @inject
    def __init__(self, building_repository: BuildingRepository) -> None:
        self.building_repository = building_repository
        
    def execute(self, data: json)->dict:
        return self.building_repository.insert_building(data=data)