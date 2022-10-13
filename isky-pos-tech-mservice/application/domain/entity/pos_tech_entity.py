from pydantic import BaseModel
from typing import Optional

class PosTechEntity(BaseModel):
    name: str
    code: str
    is_active: bool