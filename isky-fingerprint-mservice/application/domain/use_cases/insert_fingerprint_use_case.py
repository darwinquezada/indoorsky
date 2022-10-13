import json
from application.domain.repository.fingerprint_repository import FingerprintRepository
from dependency_injector.wiring import inject

class InsertFingerprintUseCase:
    @inject
    def __init__(self, fingerprint_repository: FingerprintRepository) -> None:
        self.floor_repository = fingerprint_repository
        
    def execute(self, data: json)->dict:
        return self.floor_repository.insert_fingerprint(data=data)