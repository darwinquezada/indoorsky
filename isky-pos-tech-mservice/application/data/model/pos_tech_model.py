from application.domain.entity.pos_tech_entity import PosTechEntity
import json

class PosTechModel(PosTechEntity):
    def __init__(self) -> None:
        pass
    
    def to_json(self, pos_tech_entity: PosTechEntity) -> dict:
        jsonData = {
            'name': pos_tech_entity.name,
            'code': pos_tech_entity.code,
            'is_active': pos_tech_entity.is_active
        }
        return jsonData

    def to_object(self, pos_tech: str) -> PosTechEntity:
        data_object = json.loads(pos_tech, object_hook=PosTechEntity)
        return data_object