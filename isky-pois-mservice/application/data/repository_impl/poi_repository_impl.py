import json
from application.domain.repository.poi_repository import PoiRepository
from application.data.datasource.poi_datasource import IPoiDatasource

class PoiRepositoryImpl(PoiRepository):
    def __init__(self, poi_datasource: IPoiDatasource) -> None:
        self.poi_datasource = poi_datasource
        
    def insert_poi(self, data: json) -> dict:
        return self.poi_datasource.insert_poi(data)
    
    def get_poi_by_id(self, poi_id: str) -> dict:
        return self.poi_datasource.get_poi_by_id(poi_id)
    
    def get_poi_by_name(self, name: str) -> dict:
        return self.poi_datasource.get_poi_by_name(name)
    
    def delete_poi(self, poi_id: str) -> dict:
        return self.poi_datasource.delete_poi(poi_id)
    
    def update_poi_by_id(self, poi_id: str, floor_id: str, name: str, description: str, image: str,
                         latitude: float, longitude: float, altitude: float, pos_x: float,
                         pos_y: float, pos_z: float, is_active: bool, is_public: bool) -> dict:
        return self.poi_datasource.update_poi_by_id(poi_id = poi_id, floor_id = floor_id, name = name, 
                                                    description= description, image = image, latitude = latitude, 
                                                    longitude = longitude, altitude = altitude, pos_x = pos_x, 
                                                    pos_y = pos_y, pos_z = pos_z, is_active = is_active, 
                                                    is_public = is_public)