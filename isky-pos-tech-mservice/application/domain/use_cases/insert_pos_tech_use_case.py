import json
from application.domain.repository.pos_tech_repository import PosTechRepository
from dependency_injector.wiring import inject

class InsertPosTechUseCase:
    @inject
    def __init__(self, pos_tech_repository: PosTechRepository) -> None:
        self.pos_tech_repository = pos_tech_repository
        
    def execute(self, data: json)->dict:
        return self.pos_tech_repository.insert_pos_tech(data=data)