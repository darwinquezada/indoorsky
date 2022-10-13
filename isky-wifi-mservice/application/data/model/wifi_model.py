from application.domain.entity.wifi_entity import WifiEntity
import json

class WifiModel(WifiEntity):
    def __init__(self)->None:
        pass
    
    def to_json(self, wifi_entity: WifiEntity) -> dict:
        jsonData = {
            'fingerprint_id': wifi_entity.fingerprint_id,
            'ssid': wifi_entity.ssid,
            'bssid': wifi_entity.bssid,
            'rssi': wifi_entity.rssi
        }
        return jsonData

    def to_object(self, wifi: str) -> WifiEntity:
        data_object = json.loads(wifi, object_hook=WifiEntity)
        return data_object