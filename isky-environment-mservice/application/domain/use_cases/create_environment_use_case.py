import json
from application.domain.repository.environment_repository import EnvironmentRepository
from dependency_injector.wiring import inject

class CreateEnvironmentUseCase:
    @inject
    def __init__(self, environment_repository: EnvironmentRepository) -> None:
        self.environment_repository = environment_repository
        
    def execute(self, data: json)->dict:
        return self.environment_repository.create_environment(data=data)