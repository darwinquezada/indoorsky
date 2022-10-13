from application.domain.entity.poi_entity import PoiEntity
import json

class PoiModel(PoiEntity):
    def __init__(self)->None:
        pass
    
    def to_json(self, poi_entity: PoiEntity) -> dict:
        jsonData = {
            "floor_id": poi_entity.floor_id,
            "name": poi_entity.name,
            "description": poi_entity.description,
            "image": poi_entity.image,
            "latitude": poi_entity.latitude,
            "longitude": poi_entity.longitude,
            "altitude": poi_entity.altitude,
            "pos_x": poi_entity.pos_x,
            "pos_y": poi_entity.pos_y,
            "pos_z": poi_entity.pos_z,
            "is_active": poi_entity.is_active,
            "is_public": poi_entity.is_public
        }
        return jsonData

    def to_object(self, poi: str) -> PoiEntity:
        data_object = json.loads(poi, object_hook=PoiEntity)
        return data_object