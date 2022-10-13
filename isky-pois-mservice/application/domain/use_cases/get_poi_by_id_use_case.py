import json
from application.domain.repository.poi_repository import PoiRepository
from dependency_injector.wiring import inject

class GetPoiByIdUseCase:
    @inject
    def __init__(self, poi_repository: PoiRepository) -> None:
        self.poi_repository = poi_repository
        
    def execute(self, poi_id: str) -> dict:
        return self.poi_repository.get_poi_by_id(poi_id=poi_id)