import json
from application.domain.repository.floor_repository import FloorRepository
from application.data.datasource.floor_datasource import IFloorDatasource

class FloorRepositoryImpl(FloorRepository):
    def __init__(self, floor_datasource: IFloorDatasource) -> None:
        self.floor_datasource = floor_datasource
        
    def insert_floor(self, data: json) -> dict:
        return self.floor_datasource.insert_floor(data)
    
    def get_floor_by_id(self, floor_id: str) -> dict:
        return self.floor_datasource.get_floor_by_id(floor_id)
    
    def get_floor_by_level(self, level: str) -> dict:
        return self.floor_datasource.get_floor_by_level(level=level)
    
    def delete_floor(self, floor_id: str) -> dict:
        return self.floor_datasource.delete_floor(floor_id)
    
    def update_floor_by_id(self, floor_id: str, building_id: str,
                           level: str, is_public: bool, is_active: bool) -> dict:
        return self.floor_datasource.update_floor_by_id(floor_id=floor_id, building_id=building_id,
                                                        level=level, is_public=is_public, is_active=is_active)