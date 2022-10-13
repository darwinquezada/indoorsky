import json
from application.domain.repository.fingerprint_repository import FingerprintRepository
from application.data.datasource.fingerprint_datasource import IFingerprintDatasource

class FingerprintRepositoryImpl(FingerprintRepository):
    def __init__(self, fingerprint_datasource: IFingerprintDatasource) -> None:
        self.fingerprint_datasource = fingerprint_datasource
        
    def insert_fingerprint(self, data: json) -> dict:
        return self.fingerprint_datasource.insert_fingerprint(data)
    
    def get_fingerprint_by_id(self, fp_id: str) -> dict:
        return self.fingerprint_datasource.get_fingerprint_by_id(fp_id=fp_id)
    
    def get_fingerprint_by_field(self, field: str, value: str) -> dict:
        return self.fingerprint_datasource.get_fingerprint_by_field(field, value)
    
    def delete_fingerprint_by_id(self, fp_id: str) -> dict:
        return self.fingerprint_datasource.delete_fingerprint_by_id(fp_id)
    
    def delete_fingerprint_by_field(self, field: str, value: str) -> dict:
        return self.fingerprint_datasource.delete_fingerprint_by_field(field, value)
    