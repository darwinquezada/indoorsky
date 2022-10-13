import json
from application.domain.repository.audit_repository import AuditRepository
from dependency_injector.wiring import inject

class InsertAuditUseCase:
    @inject
    def __init__(self, audit_repository: AuditRepository) -> None:
        self.audit_repository = audit_repository
        
    def execute(self, data: json)->dict:
        return self.audit_repository.insert_audit(data=data)