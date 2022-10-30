import json
from application.domain.repository.positioning_repository import PositioningRepository
from dependency_injector.wiring import inject

class DeleteSetModelUseCase:
    @inject
    def __init__(self, positioning_repository: PositioningRepository) -> None:
        self.positioning_repository = positioning_repository
        
    def execute(self, set_model_id: str)->dict:
        return self.positioning_repository.delete_set_model(set_model_id=set_model_id)