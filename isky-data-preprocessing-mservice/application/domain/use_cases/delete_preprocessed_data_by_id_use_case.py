from application.domain.repository.preprocessing_repository import PreprocessingRepository
from dependency_injector.wiring import inject

class DeletePreprocessedDataByIdUseCase:
    @inject
    def __init__(self, preprocessing_repository: PreprocessingRepository) -> None:
        self.preprocessing_repository = preprocessing_repository
        
    def execute(self, conf_prepro_id: str) -> dict:
        return self.preprocessing_repository.delete_data_preprocessed_by_id(conf_prepro_id=conf_prepro_id)