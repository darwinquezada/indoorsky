from application.domain.entity.floor_entity import FloorEntity
import json

class FloorModel(FloorEntity):
    def __init__(self) -> None:
        pass
    
    def to_json(self, floor_entity: FloorEntity) -> dict:
        jsonData = {
            'building_id': floor_entity.building_id,
            'level': floor_entity.level,
            'is_public': floor_entity.is_public,
            'is_active': floor_entity.is_active
        }
        return jsonData

    def to_object(self, floor: str) -> FloorEntity:
        data_object = json.loads(floor, object_hook=FloorEntity)
        return data_object