import json
from application.domain.repository.environment_repository import EnvironmentRepository
from application.data.datasource.environment_datasource import IEnvironmentDatasource

class EnvironmentRepositoryImpl(EnvironmentRepository):
    def __init__(self, environment_datasource: IEnvironmentDatasource) -> None:
        self.environment_datasource = environment_datasource
    
    def create_environment(self, data: json) -> dict:
        return self.environment_datasource.create_environment(data=data)
    
    def get_environments(self) -> dict:
        return self.environment_datasource.get_environments()
    
    def get_environment_by_id(self, env_id: str) -> dict:
        return self.environment_datasource.get_environment_by_id(env_id=env_id)
    
    def get_environment_by_name(self, name: str) -> dict:
        return self.environment_datasource.get_environment_by_name(name=name)
    
    def delete_environment(self, env_id: str) -> dict:
        return self.environment_datasource.delete_environment(env_id=env_id)
    
    def update_environment(self, env_id: str, name: str, address: str, 
                           num_buildings: int, is_public: bool, 
                           is_active: bool) -> dict:
        return self.environment_datasource.update_environment(env_id=env_id, name=name, 
                                                              address=address, num_buildings=num_buildings, 
                                                              is_public=is_public, 
                                                              is_active=is_active)
    