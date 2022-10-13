from application.domain.entity.audit_entity import AuditEntity
import json

class FloorModel(AuditEntity):
    def __init__(self) -> None:
        pass
    
    def to_json(self, audit_entity: AuditEntity) -> dict:
        jsonData = {
            'user_id': audit_entity.user_id,
            'local_ip': audit_entity.local_ip,
            'external_ip': audit_entity.external_ip,
            'event': audit_entity.event,
            'description': audit_entity.description
        }
        return jsonData

    def to_object(self, audit: str) -> AuditEntity:
        data_object = json.loads(audit, object_hook=AuditEntity)
        return data_object