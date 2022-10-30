import json
from application.domain.repository.positioning_repository import PositioningRepository
from dependency_injector.wiring import inject

class GetSetModelByModelTypeUseCase:
    @inject
    def __init__(self, positioning_repository: PositioningRepository) -> None:
        self.positioning_repository = positioning_repository
        
    def execute(self, model_type: str)->dict:
        return self.positioning_repository.get_set_model_by_model_type(model_type=model_type)