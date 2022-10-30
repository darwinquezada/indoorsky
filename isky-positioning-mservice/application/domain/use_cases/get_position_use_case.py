import json
from application.domain.repository.positioning_repository import PositioningRepository
from dependency_injector.wiring import inject

class GetPositionUseCase:
    @inject
    def __init__(self, positioning_repository: PositioningRepository) -> None:
        self.positioning_repository = positioning_repository
        
    def execute(self, pos_tech_id:str, model_type: str, data: json)->dict:
        return self.positioning_repository.get_position(pos_tech_id=pos_tech_id, model_type=model_type, data=data)