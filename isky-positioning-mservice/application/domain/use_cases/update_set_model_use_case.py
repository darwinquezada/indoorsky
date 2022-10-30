import json
from application.domain.repository.positioning_repository import PositioningRepository
from dependency_injector.wiring import inject

class UpdateSetModelUseCase:
    @inject
    def __init__(self, positioning_repository: PositioningRepository) -> None:
        self.positioning_repository = positioning_repository
        
    def execute(self, set_model_id: str, model: json)->dict:
        return self.positioning_repository.update_set_model(set_model_id=set_model_id, model=model)