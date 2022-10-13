import json
from application.domain.repository.pos_tech_repository import PosTechRepository
from dependency_injector.wiring import inject

class GetPosTechByNamePosTechUseCase:
    @inject
    def __init__(self, pos_tech_repository: PosTechRepository) -> None:
        self.pos_tech_repository = pos_tech_repository
        
    def execute(self, name: str)->dict:
        return self.pos_tech_repository.get_pos_tech_by_name(name=name)