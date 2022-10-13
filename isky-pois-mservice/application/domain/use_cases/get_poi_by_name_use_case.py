import json
from application.domain.repository.poi_repository import PoiRepository
from dependency_injector.wiring import inject

class GetPoiByNameUseCase:
    @inject
    def __init__(self, poi_repository: PoiRepository) -> None:
        self.poi_repository = poi_repository
        
    def execute(self, name: str) -> dict:
        return self.poi_repository.get_poi_by_name(name=name)