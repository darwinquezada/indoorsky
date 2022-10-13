from application.domain.entity.preprocessing_entity import PreprocessingEntity
import json

class FloorModel(PreprocessingEntity):
    def __init__(self) -> None:
        pass
    
    def to_json(self, preprocessing_entity: PreprocessingEntity) -> dict:
        jsonData = {
            'env_id': preprocessing_entity.env_id,
            'type_id': preprocessing_entity.type,
            'pos_technology': preprocessing_entity.pos_technology,
            'defoult_non_dec_val': preprocessing_entity.defoult_non_dec_val,
            'non_dec_val': preprocessing_entity.non_dec_val,
            'is_active': preprocessing_entity.is_active,
        }
        return jsonData

    def to_object(self, preprocessing: str) -> PreprocessingEntity:
        data_object = json.loads(preprocessing, object_hook=PreprocessingEntity)
        return data_object