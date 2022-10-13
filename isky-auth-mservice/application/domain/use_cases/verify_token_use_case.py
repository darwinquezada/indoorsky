from application.domain.respositories.verify_token import VerifyToken
from dependency_injector.wiring import inject

class VerifyTokenUseCase:
    @inject
    def __init__(self, token_repository: VerifyToken):
        self.token_repository = token_repository
    
    def execute(self, endpoint: str, project_id: str, jwt_token: str) -> dict:
        return self.token_repository.verify(endpoint=endpoint, project_id=project_id, jwt_token=jwt_token)