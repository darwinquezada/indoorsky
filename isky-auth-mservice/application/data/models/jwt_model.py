from application.domain.entities.jwt_entity import JWTEntity
import json

class JWTModel(JWTEntity):
    def __init__(self) -> None:
        pass
    
    def to_json(self, jwt_entity: JWTEntity) -> dict:
        """
        Convert Entity to dict
        Input:
        jwt_entity: JWTEntity class
        """
        jsonData = {
            "jwt_key": jwt_entity.jwt_key
        }
        return jsonData

    def to_object(self, jwt_entity: str) -> JWTEntity:
        """
        Convert string to JWTEntity
        """
        parameters_object = json.loads(jwt_entity, object_hook=JWTEntity)
        return parameters_object