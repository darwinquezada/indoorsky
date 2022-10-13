from pydantic import BaseModel


class JWTEntity(BaseModel):
    jwt_key: str