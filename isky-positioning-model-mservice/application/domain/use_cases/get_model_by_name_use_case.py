import json
from application.domain.repository.model_repository import ModelRepository
from dependency_injector.wiring import inject

class GetModelByNameUseCase:
    @inject
    def __init__(self, model_repository: ModelRepository) -> None:
        self.model_repository = model_repository
        
    def execute(self, name: str)->dict:
        return self.model_repository.get_model_by_name(name=name)