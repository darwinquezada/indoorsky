from application.domain.entity.building_entity import BuildingEntity
import json

class BuildingModel(BuildingEntity):
    def __init__(self)->None:
        pass
    
    def to_json(self, building_entity: BuildingEntity) -> dict:
        jsonData = {
            'env_id': building_entity.env_id, 
            'name': building_entity.name, 
            'num_floors': building_entity.num_floors, 
            'description': building_entity.description,
            'latitude': building_entity.latitude, 
            'longitude': building_entity.longitude, 
            'altitude': building_entity.altitude,
            'is_public': building_entity.is_public, 
            'is_active': building_entity.is_active
        }
        return jsonData

    def to_object(self, user: str) -> BuildingEntity:
        data_object = json.loads(user, object_hook=BuildingEntity)
        return data_object