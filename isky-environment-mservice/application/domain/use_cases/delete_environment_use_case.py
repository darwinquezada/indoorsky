import json
from application.domain.repository.environment_repository import EnvironmentRepository
from dependency_injector.wiring import inject

class DeleteEnvironmentUseCase:
    @inject
    def __init__(self, environment_repository: EnvironmentRepository) -> None:
        self.environment_repository = environment_repository
        
    def execute(self, env_id: str)->dict:
        return self.environment_repository.delete_environment(env_id=env_id)