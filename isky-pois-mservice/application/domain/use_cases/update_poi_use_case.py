import json
from application.domain.repository.poi_repository import PoiRepository
from dependency_injector.wiring import inject

class UpdatePoiUseCase:
    @inject
    def __init__(self, poi_repository: PoiRepository) -> None:
        self.poi_repository = poi_repository
        
    def execute(self, poi_id: str, floor_id: str, name: str, description: str, 
                image: str, latitude: float, longitude: float, altitude: float, 
                pos_x: float, pos_y: float, pos_z: float, is_active: bool, 
                is_public: bool) -> dict:
        return self.poi_repository.update_poi_by_id(poi_id = poi_id, floor_id = floor_id, name = name, 
                                                    description= description, image = image, latitude = latitude, 
                                                    longitude = longitude, altitude = altitude, pos_x = pos_x, 
                                                    pos_y = pos_y, pos_z = pos_z, is_active = is_active, 
                                                    is_public = is_public)