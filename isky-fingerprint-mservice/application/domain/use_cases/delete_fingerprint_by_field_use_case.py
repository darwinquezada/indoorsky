from application.domain.repository.fingerprint_repository import FingerprintRepository
from dependency_injector.wiring import inject

class DeleteFingerprintByFieldUseCase:
    @inject
    def __init__(self, fingerprint_repository: FingerprintRepository) -> None:
        self.fingerprint_repository = fingerprint_repository
        
    def execute(self, field: str, value: str) -> dict:
        return self.fingerprint_repository.delete_fingerprint_by_field(field=field, value=value)