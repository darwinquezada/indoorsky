from abc import ABC, abstractmethod

class IUserDatasource(ABC):
    
    @abstractmethod
    def create_user(self, name: str, email: str, password: str) -> dict:
        pass
    
    @abstractmethod
    def get_user(self, user_id: str) -> dict:
        pass
    
    @abstractmethod
    def delete_user(self, user_id: str) -> dict:
        pass
    
    @abstractmethod
    def update_user_name(self, user_id: str, name: str) -> dict:
        pass
    
    @abstractmethod
    def update_user_email(self, user_id: str, email: str) -> dict:
        pass
    
    @abstractmethod
    def update_user_password(self, user_id: str, password: str) -> dict:
        pass
    
    @abstractmethod
    def update_user_phone(self, user_id: str, phone: str) -> dict:
        pass
    
    @abstractmethod
    def update_user_email_verification(self, user_id: str, verify: bool) -> dict:
        pass
    
    @abstractmethod
    def update_user_phone_verification(self, user_id: str, verify: bool) -> dict:
        pass
    
    @abstractmethod
    def update_user_status(self, user_id: str, status: bool) -> dict:
        pass