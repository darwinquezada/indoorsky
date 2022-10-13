from pydantic import BaseModel

from flask_openapi3 import Info, Tag
from flask_openapi3 import OpenAPI, APIBlueprint
from pydantic import BaseModel, Field
from application.presentation.endpoints import url_prefix, Unauthorized

auth_tag = Tag(name='Auth', description='Auth API endpoints')

api_auth = APIBlueprint(
    '/auth',
    __name__,
    url_prefix=url_prefix,
    abp_tags=[auth_tag],
    # abp_security=security,
    abp_responses={"401": Unauthorized},
    doc_ui=True
)

from application.presentation.endpoints.authentication import authentication_endpoints
