from pydantic import BaseModel

class UserEntity(BaseModel):
    name: str
    email: str
    password: str
    