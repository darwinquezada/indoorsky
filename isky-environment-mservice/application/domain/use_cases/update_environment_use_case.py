import json
from application.domain.repository.environment_repository import EnvironmentRepository
from dependency_injector.wiring import inject

class UpdateEnvironmentUseCase:
    @inject
    def __init__(self, environment_repository: EnvironmentRepository) -> None:
        self.environment_repository = environment_repository
        
    def execute(self, env_id:str, name: str, address: str, 
                num_buildings:int, is_public:bool, 
                is_active: bool)->dict:
        return self.environment_repository.update_environment(env_id=env_id, name=name, address=address, 
                           num_buildings=num_buildings, is_public=is_public, 
                           is_active=is_active)