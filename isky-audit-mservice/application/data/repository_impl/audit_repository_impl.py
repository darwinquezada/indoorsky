import json
from application.domain.repository.audit_repository import AuditRepository
from application.data.datasource.audit_datasource import IAuditDatasource

class AuditRepositoryImpl(AuditRepository):
    def __init__(self, audit_datasource: IAuditDatasource) -> None:
        self.audit_datasource = audit_datasource
        
    def insert_audit(self, data: json) -> dict:
        """
        Implementing insert logs to audit table
        """
        return self.audit_datasource.insert_audit(data)
    
    def get_audit_by_user_id(self, user_id: str) -> dict:
        """
        Implementing, get audit by user ID
        """
        return self.audit_datasource.get_audit_by_user_id(user_id=user_id)
    
   