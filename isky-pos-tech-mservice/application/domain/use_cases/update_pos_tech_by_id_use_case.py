import json
from application.domain.repository.pos_tech_repository import PosTechRepository
from dependency_injector.wiring import inject

class UpdatePosTechByIdPosTechUseCase:
    @inject
    def __init__(self, pos_tech_repository: PosTechRepository) -> None:
        self.pos_tech_repository = pos_tech_repository
        
    def execute(self, pos_tech_id: str, data: json)->dict:
        return self.pos_tech_repository.update_pos_tech_by_id(pos_tech_id=pos_tech_id, data=data)