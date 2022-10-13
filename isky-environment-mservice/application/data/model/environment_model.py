from application.domain.entity.environment_entity import EnvironmentEntity
import json

class EnvironmentModel(EnvironmentEntity):
    def __init__(self)->None:
        pass
    
    def to_json(self, environment_entity: EnvironmentEntity) -> dict:
        jsonData = {
            "name": environment_entity.name,
            "address": environment_entity.address,
            "num_buildings": environment_entity.num_buildings,
            "is_public": environment_entity.is_public,
            "is_active": environment_entity.is_active
        }
        return jsonData

    def to_object(self, user: str) -> EnvironmentEntity:
        data_object = json.loads(user, object_hook=EnvironmentEntity)
        return data_object