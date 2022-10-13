from application.domain.repository.user_repository import UserRepository
from dependency_injector.wiring import inject


class UpdateUserEmailUseCase:
    @inject
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, user_id: str, email: str) -> dict:
        return self.user_repository.update_user_email(user_id=user_id, email=email)