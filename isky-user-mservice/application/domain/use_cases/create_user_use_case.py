from application.domain.repository.user_repository import UserRepository
from dependency_injector.wiring import inject


class CreateUserUseCase:
    @inject
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, name: str, email: str, password: str) -> dict:
        return self.user_repository.create_user(name, email, password)