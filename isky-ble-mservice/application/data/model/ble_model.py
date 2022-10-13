from application.domain.entity.ble_entity import BleEntity
import json

class BleModel(BleEntity):
    def __init__(self)->None:
        pass
    
    def to_json(self, ble_entity: BleEntity) -> dict:
        jsonData = {
            'fingerprint_id': ble_entity.fingerprint_id,
            'device_id': ble_entity.device_id,
            'name': ble_entity.name,
            'rssi': ble_entity.rssi
        }
        return jsonData

    def to_object(self, ble: str) -> BleEntity:
        data_object = json.loads(ble, object_hook=BleEntity)
        return data_object