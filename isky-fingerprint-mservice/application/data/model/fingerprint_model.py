from application.domain.entity.fingerprint_entity import FingerprintEntity
import json

class FingerprintModel(FingerprintEntity):
    def __init__(self)->None:
        pass
    
    def to_json(self, fingerprint_entity: FingerprintEntity) -> dict:
        jsonData = {
            'user_device': fingerprint_entity.user_device,
            'os': fingerprint_entity.os,
            'version': fingerprint_entity.version,
            'env_id': fingerprint_entity.env_id,
            'building_id': fingerprint_entity.building_id,
            'floor_id': fingerprint_entity.floor_id,
            'poi_id': fingerprint_entity.poi_id
        }
        return jsonData

    def to_object(self, fingerprint: str) -> FingerprintEntity:
        data_object = json.loads(fingerprint, object_hook=FingerprintEntity)
        return data_object