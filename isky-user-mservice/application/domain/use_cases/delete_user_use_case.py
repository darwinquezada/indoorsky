from application.domain.repository.user_repository import UserRepository
from dependency_injector.wiring import inject


class DeleteUserUseCase:
    @inject
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, user_id: str) -> dict:
        return self.user_repository.delete_user(user_id=user_id)