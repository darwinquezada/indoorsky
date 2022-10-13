import json
from application.domain.repository.cleansing_repository import DataCleansingRepository
from application.data.datasource.cleansing_datasource import IDataCleansingDatasource

class DataCleansingRepositoryImpl(DataCleansingRepository):
    def __init__(self, cleansing_datasource: IDataCleansingDatasource) -> None:
        self.cleansing_datasource = cleansing_datasource
        
    def clean_dataset(self, data: json) -> dict:
        return self.cleansing_datasource.clean_dataset(data)
    
    def get_cleansed_dataset_by_id(self, clean_id: str) -> dict:
        return self.cleansing_datasource.get_cleansed_dataset_by_id(clean_id)
    
    def get_cleansed_dataset_by_env(self, env_id: str) -> dict:
        return self.cleansing_datasource.get_cleansed_dataset_by_env(env_id)
    
    def get_cleansed_dataset_by_name(self, name: str) -> dict:
        return self.cleansing_datasource.get_cleansed_dataset_by_name(name)
    
    def delete_cleansed_dataset(self, clean_id: str) -> dict:
        return self.cleansing_datasource.delete_cleansed_dataset(clean_id)
    