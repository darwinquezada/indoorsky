from application.domain.repository.model_repository import ModelRepository
from dependency_injector.wiring import inject

class DeleteModelByIdUseCase:
    @inject
    def __init__(self, model_repository: ModelRepository) -> None:
        self.model_repository = model_repository
        
    def execute(self, model_id: str)->dict:
        return self.model_repository.get_model_by_id(model_id=model_id)