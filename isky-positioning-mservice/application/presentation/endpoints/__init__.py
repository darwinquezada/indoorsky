from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from application.presentation import url_prefix, security, Unauthorized

positioning_tag = Tag(name='Positioning', description='Positioning API endpoints')

api_positioning = APIBlueprint(
    '/positioning',
    __name__,
    url_prefix=url_prefix,
    abp_tags=[positioning_tag],
    abp_security=security,
    abp_responses={"401": Unauthorized},
    doc_ui=True
)

from application.presentation.endpoints import positioning_endpoints