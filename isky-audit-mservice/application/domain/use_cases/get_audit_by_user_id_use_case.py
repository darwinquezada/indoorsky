from application.domain.repository.audit_repository import AuditRepository
from dependency_injector.wiring import inject

class GetAuditByUserIdUseCase:
    @inject
    def __init__(self, audit_repository: AuditRepository) -> None:
        self.audit_repository = audit_repository
        
    def execute(self, user_id: str) -> dict:
        return self.audit_repository.get_audit_by_user_id(user_id=user_id)