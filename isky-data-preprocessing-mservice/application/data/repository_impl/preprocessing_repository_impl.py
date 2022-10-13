import json
from application.domain.repository.preprocessing_repository import PreprocessingRepository
from application.data.datasource.preprocessing_datasource import IPreprocessingDatasource

class PreprocessingRepositoryImpl(PreprocessingRepository):
    def __init__(self, preprocessing_datasource: IPreprocessingDatasource) -> None:
        self.preprocessing_datasource = preprocessing_datasource
        
    def get_data_preprocessed_by_id(self, conf_prepro_id: str) -> dict:
        return self.preprocessing_datasource.get_data_preprocessed_by_id(conf_prepro_id)
    
    def preprocess_data(self, data: json) -> dict:
        return self.preprocessing_datasource.preprocess_data(data)
    
    def delete_data_preprocessed_by_id(self, conf_prepro_id: str) -> dict:
        return self.preprocessing_datasource.delete_data_preprocessed_by_id(conf_prepro_id)
    
    def get_data_preprocessed_by_env(self, env_id: str) -> dict:
        return self.preprocessing_datasource.get_data_preprocessed_by_env(env_id)