from application.domain.entity.user_entity import UserEntity
import json


class UserModel(UserEntity):
    def __init__(self) -> None:
        pass

    def to_json(self, user_entity: UserEntity) -> dict:
        jsonData = {
            "name": user_entity.name,
            "email": user_entity.email,
            "password": user_entity.password
        }
        return jsonData

    def to_object(self, user: str) -> UserEntity:
        algorithm_object = json.loads(user, object_hook=UserEntity)
        return algorithm_object