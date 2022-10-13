from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from application.presentation import url_prefix, security, Unauthorized

building_tag = Tag(name='Building', description='Building API Endpoints')

api_building = APIBlueprint(
    '/building',
    __name__,
    url_prefix=url_prefix,
    abp_tags=[building_tag],
    abp_security=security,
    abp_responses={"401": Unauthorized},
    doc_ui=True
)

from application.presentation.endpoints import building_endpoints
