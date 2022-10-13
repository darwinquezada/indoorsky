import json
from application.domain.repository.environment_repository import EnvironmentRepository
from dependency_injector.wiring import inject

class GetEnvironmentByIdUseCase:
    @inject
    def __init__(self, environment_repository: EnvironmentRepository) -> None:
        self.environment_repository = environment_repository
        
    def execute(self, env_id: str)->dict:
        return self.environment_repository.get_environment_by_id(env_id=env_id)