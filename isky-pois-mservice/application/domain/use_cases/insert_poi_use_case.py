import json
from application.domain.repository.poi_repository import PoiRepository
from dependency_injector.wiring import inject

class InsertPoiUseCase:
    @inject
    def __init__(self, poi_repository: PoiRepository) -> None:
        self.poi_repository = poi_repository
        
    def execute(self, data: json)->dict:
        return self.poi_repository.insert_poi(data=data)