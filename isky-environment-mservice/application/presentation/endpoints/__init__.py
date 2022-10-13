from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from application.presentation import url_prefix, security, Unauthorized

environment_tag = Tag(name='Environment', description='Environment API Endpoints')

api_environment = APIBlueprint(
    '/environment',
    __name__,
    url_prefix=url_prefix,
    abp_tags=[environment_tag],
    abp_security=security,
    abp_responses={"401": Unauthorized},
    doc_ui=True
)

from application.presentation.endpoints import environment_endpoints
