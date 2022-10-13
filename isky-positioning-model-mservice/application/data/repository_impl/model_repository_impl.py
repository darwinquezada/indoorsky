import json
from application.domain.repository.model_repository import ModelRepository
from application.data.datasource.model_datasource import IModelDatasource

class ModelRepositoryImpl(ModelRepository):
    def __init__(self, model_datasource: IModelDatasource) -> None:
        self.model_datasource = model_datasource
        
    def train_model(self, data: json, model: str) -> dict:
        return self.model_datasource.train_model(data, model)
    
    def get_model_by_id(self, model_id: str) -> dict:
        return self.model_datasource.get_model_by_id(model_id)
    
    def get_model_by_name(self, name: str) -> dict:
        return self.model_datasource.get_model_by_name(name)
    
    def delete_model_by_id(self, model_id: str) -> dict:
        return self.model_datasource.delete_model_by_id(model_id=model_id)