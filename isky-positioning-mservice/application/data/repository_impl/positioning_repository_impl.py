import json
from application.domain.repository.positioning_repository import PositioningRepository
from application.data.data_source.positioning_datasource import IPositioningDatasource

class PositioningRepositoryImpl(PositioningRepository):
    def __init__(self, positioning_datasource: IPositioningDatasource) -> None:
        self.positioning_datasource = positioning_datasource
        
    def get_position(self, pos_tech_id:str, model_type:str, data: json) -> dict:
        return self.positioning_datasource.get_position(pos_tech_id=pos_tech_id, model_type=model_type, data=data)
    
    def set_models(self, model: json) -> dict:
        return self.positioning_datasource.set_models(model=model)
    
    def delete_set_model(self, set_model_id: str) -> dict:
        return self.positioning_datasource.delete_set_model(set_model_id)
    
    def update_set_model(self, set_model_id: str, model: json) -> dict:
        return self.positioning_datasource.update_set_model(set_model_id, model)
    
    def get_set_model_by_model_type(self, model_type: str) -> dict:
        return self.positioning_datasource.get_set_model_by_model_type(model_type)