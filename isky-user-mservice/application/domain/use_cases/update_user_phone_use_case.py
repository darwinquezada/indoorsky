from application.domain.repository.user_repository import UserRepository
from dependency_injector.wiring import inject


class UpdateUserPhoneUseCase:
    @inject
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, user_id: str, phone: str) -> dict:
        return self.user_repository.update_user_phone(user_id=user_id, phone=phone)