from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from application.presentation import url_prefix, security, Unauthorized

user_tag = Tag(name='User', description='User API endpoints')

api_user = APIBlueprint(
    '/user',
    __name__,
    url_prefix=url_prefix,
    abp_tags=[user_tag],
    abp_security=security,
    abp_responses={"401": Unauthorized},
    doc_ui=True
)

from application.presentation.endpoints import user_endpoints
