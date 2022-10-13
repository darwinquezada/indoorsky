from application.domain.repository.preprocessing_repository import PreprocessingRepository
from dependency_injector.wiring import inject

class GetPreprocessedDataByEnvUseCase:
    @inject
    def __init__(self, preprocessing_repository: PreprocessingRepository) -> None:
        self.preprocessing_repository = preprocessing_repository
        
    def execute(self, env_id: str) -> dict:
        return self.preprocessing_repository.get_data_preprocessed_by_env(env_id=env_id)