from application.domain.repository.user_repository import UserRepository
from dependency_injector.wiring import inject


class UpdateUserStatusUseCase:
    @inject
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, user_id: str, status: bool) -> dict:
        return self.user_repository.update_user_status(user_id=user_id, status=status)