import os
from . import api_auth, auth_tag
from pydantic import BaseModel, Field
from application.domain.entities.jwt_entity import JWTEntity
from application.data.models.jwt_model import JWTModel
from application.domain.use_cases.verify_token_use_case import VerifyTokenUseCase
from ...data_injection.injection_container import ApplicationContainer
# from application.core.decorators.jwt_manager import login_required

dotenv_path = os.path.join(os.getcwd(), '.env')

class Path(BaseModel):
    token: str = Field(..., description='Token')

@api_auth.get('/auth/<token>', tags=[auth_tag])
def verify_token(path: Path):
    endpoint = os.environ['APPWRITEENDPOINT']
    project_id = os.environ['APPWRITEPROJECTID']
    verify_token_use_case = VerifyTokenUseCase(token_repository=ApplicationContainer.repository()) # algorithm_repository=ApplicationContainer.repository_algorithms())
    return verify_token_use_case.execute(endpoint=endpoint, project_id=project_id, jwt_token=path.token)

