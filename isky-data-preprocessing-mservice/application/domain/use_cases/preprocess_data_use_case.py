from application.domain.repository.preprocessing_repository import PreprocessingRepository
from dependency_injector.wiring import inject
import json

class PreprocessDataUseCase:
    @inject
    def __init__(self, preprocessing_repository: PreprocessingRepository) -> None:
        self.preprocessing_repository = preprocessing_repository
        
    def execute(self, data: json) -> dict:
        return self.preprocessing_repository.preprocess_data(data=data)