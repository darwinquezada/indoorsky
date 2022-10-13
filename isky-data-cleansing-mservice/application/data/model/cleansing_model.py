from application.domain.entity.cleansing_entity import CleansingEntity
import json

class CleansingModel(CleansingEntity):
    def __init__(self)->None:
        pass
    
    def to_json(self, cleansing_entity: CleansingEntity) -> dict:
        jsonData = {
            'name': cleansing_entity.name,
            'threshold': cleansing_entity.threshold,
            'dataset_id': cleansing_entity.dataset_id,
            'test': cleansing_entity.test
        }
        return jsonData

    def to_object(self, cleansing: str) -> CleansingEntity:
        data_object = json.loads(cleansing, object_hook=CleansingEntity)
        return data_object