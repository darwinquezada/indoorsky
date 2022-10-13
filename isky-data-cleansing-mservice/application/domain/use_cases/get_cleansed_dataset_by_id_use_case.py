from application.domain.repository.cleansing_repository import DataCleansingRepository
from dependency_injector.wiring import inject

class GetCleansedDatasetByIdUseCase:
    @inject
    def __init__(self, cleansing_repository: DataCleansingRepository) -> None:
        self.cleansing_repository = cleansing_repository
        
    def execute(self, clean_id: str)->dict:
        return self.cleansing_repository.get_cleansed_dataset_by_id(clean_id=clean_id)