import json
from application.domain.repository.positioning_repository import PositioningRepository
from dependency_injector.wiring import inject

class SetPositionModelUseCase:
    @inject
    def __init__(self, positioning_repository: PositioningRepository) -> None:
        self.positioning_repository = positioning_repository
        
    def execute(self, model: json)->dict:
        return self.positioning_repository.set_models(model=model)