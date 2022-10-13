from abc import ABC, abstractmethod


class VerifyToken(ABC):
    
    @abstractmethod
    def verify(self, endpoint: str, project_id: str, jwt_token: str) -> dict:
        pass
    