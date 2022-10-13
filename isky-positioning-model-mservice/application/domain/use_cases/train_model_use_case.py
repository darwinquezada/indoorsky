import json
from application.domain.repository.model_repository import ModelRepository
from dependency_injector.wiring import inject

class TrainModelUseCase:
    @inject
    def __init__(self, model_repository: ModelRepository) -> None:
        self.model_repository = model_repository
        
    def execute(self, data: json, model: str)->dict:
        return self.model_repository.train_model(data=data, model=model)