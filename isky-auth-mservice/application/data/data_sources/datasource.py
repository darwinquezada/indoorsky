from abc import ABC, abstractmethod


class IDataSource(ABC):
    """
    Interface Data source
    """
    @abstractmethod
    def verify_token(self, endpoint: str, project_id: str, jwt_token: str) -> dict:
        pass