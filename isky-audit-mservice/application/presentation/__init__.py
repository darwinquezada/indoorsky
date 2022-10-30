from pydantic import BaseModel

from flask_openapi3 import Info
from flask_openapi3 import OpenAPI
from pydantic import BaseModel, Field

from application.core.exceptions.status_codes import (MethodNotAllowedResponseCode,NotFoundResponseCode)

from flask_openapi3.models.security import HTTPBearer, OAuth2, OAuthFlows, OAuthFlowImplicit

jwt = HTTPBearer(bearerFormat="JWT")
oauth2 = OAuth2(flows=OAuthFlows(
    implicit=OAuthFlowImplicit(
        authorizationUrl="https://example.com/api/oauth/dialog",
        scopes={
            "write:user": "modify users",
            "read:user": "read your users"
        }
    )))
security_schemes = {"jwt": jwt}
security = [{"jwt": []}]

class NotFoundResponse(BaseModel):
    NotFoundResponseCode()

class Unauthorized(BaseModel):
    code: int = Field(-1, description="Status Code")
    message: str = Field("Unauthorized!", description="Exception Information.")

url_prefix = '/api/v1'

info = Info(title='Indoor Positioning API', version='1.0.0')
app = OpenAPI(__name__, info=info, security_schemes=security_schemes)