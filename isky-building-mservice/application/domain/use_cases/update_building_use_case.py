import json
from application.domain.repository.building_repository import BuildingRepository
from dependency_injector.wiring import inject

class UpdateBuildingUseCase:
    @inject
    def __init__(self, building_repository: BuildingRepository) -> None:
        self.building_repository = building_repository
        
    def execute(self, building_id: str, env_id: str, name: str, num_floors: int, description: str,
                latitude: float, longitude: float, altitude: float, is_public: bool, is_active: bool) -> dict:
        return self.building_repository.update_building_by_id(building_id=building_id, env_id=env_id, 
                              name=name, num_floors=num_floors, description=description,
                              latitude=latitude, longitude=longitude, altitude=altitude,
                              is_public=is_public, is_active=is_active)