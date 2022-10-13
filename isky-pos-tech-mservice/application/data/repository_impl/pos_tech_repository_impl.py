import json
from application.domain.repository.pos_tech_repository import PosTechRepository
from application.data.datasource.pos_tech_datasource import IPosTechDatasource

class PosTechRepositoryImpl(PosTechRepository):
    def __init__(self, pos_tech_datasource: IPosTechDatasource) -> None:
        self.pos_tech_datasource = pos_tech_datasource
        
    def insert_pos_tech(self, data: json) -> dict:
        return self.pos_tech_datasource.insert_pos_tech(data)
    
    def get_pos_tech_by_id(self, pos_tech_id: str) -> dict:
        return self.pos_tech_datasource.get_pos_tech_by_id(pos_tech_id)
    
    def get_pos_tech_by_name(self, name: str) -> dict:
        return self.pos_tech_datasource.get_pos_tech_by_name(name)
    
    def update_pos_tech_by_id(self, pos_tech_id: str, data: json) -> dict:
        return self.pos_tech_datasource.update_pos_tech_by_id(pos_tech_id, data)
    
    def delete_pos_tech_by_id(self, pos_tech_id: str) -> dict:
        return self.pos_tech_datasource.delete_pos_tech_by_id(pos_tech_id)