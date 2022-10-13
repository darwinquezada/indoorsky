import json
from application.domain.repository.cleansing_repository import DataCleansingRepository
from dependency_injector.wiring import inject

class DataCleansingUseCase:
    @inject
    def __init__(self, cleansing_repository: DataCleansingRepository) -> None:
        self.cleansing_repository = cleansing_repository
        
    def execute(self, data: json)->dict:
        return self.cleansing_repository.clean_dataset(data=data)