from application.domain.repository.user_repository import UserRepository
from application.data.datasource.user_datasource import IUserDatasource

class UserRepositoryImpl(UserRepository):
    def __init__(self, user_datasource: IUserDatasource) -> None:
        print(type(user_datasource))
        self.user_datasource = user_datasource
        
    def create_user(self, name: str, email: str, password: str) -> dict:
        return self.user_datasource.create_user(name, email, password)
    
    def get_user(self, user_id: str) -> dict:
        return self.user_datasource.get_user(user_id=user_id)
    
    def delete_user(self, user_id: str) -> dict:
        return self.user_datasource.delete_user(user_id=user_id)
    
    def update_user_name(self, user_id: str, name: str) -> dict:
        return self.user_datasource.update_user_name(user_id, name)
    
    def update_user_email(self, user_id: str, email: str) -> dict:
        return self.user_datasource.update_user_email(user_id, email)
    
    def update_user_password(self, user_id: str, password: str) -> dict:
        return self.user_datasource.update_user_password(user_id, password)
    
    def update_user_phone(self, user_id: str, phone: str) -> dict:
        return self.user_datasource.update_user_phone(user_id, phone)
    
    def update_user_email_verification(self, user_id: str, verify: bool) -> dict:
        return self.user_datasource.update_user_email_verification(user_id, verify)
    
    def update_user_phone_verification(self, user_id: str, verify: bool) -> dict:
        return self.user_datasource.update_user_phone_verification(user_id, verify)
    
    def update_user_status(self, user_id: str, status: bool) -> dict:
        return self.user_datasource.update_user_status(user_id, status)