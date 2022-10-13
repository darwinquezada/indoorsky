import json
from application.domain.repository.building_repository import BuildingRepository
from application.data.datasource.building_datasource import IBuildingDatasource

class BuildingRepositoryImpl(BuildingRepository):
    def __init__(self, building_datasource: IBuildingDatasource) -> None:
        self.building_datasource = building_datasource
        
    def insert_building(self, data: json) -> dict:
        return self.building_datasource.insert_building(data)
    
    def get_building_by_id(self, building_id: str) -> dict:
        return self.building_datasource.get_building_by_id(building_id)
    
    def get_building_by_name(self, name: str) -> dict:
        return self.building_datasource.get_building_by_name(name)
    
    def delete_building(self, building_id: str) -> dict:
        return self.building_datasource.delete_building(building_id)
    
    def update_building_by_id(self, building_id: str, env_id: str, 
                              name: str, num_floors: int, description: str,
                              latitude: float, longitude: float, altitude: float,
                              is_public: bool, is_active: bool) -> dict:
        return self.building_datasource.update_building_by_id(building_id=building_id, env_id=env_id, 
                              name=name, num_floors=num_floors, description=description,
                              latitude=latitude, longitude=longitude, altitude=altitude,
                              is_public=is_public, is_active=is_active)