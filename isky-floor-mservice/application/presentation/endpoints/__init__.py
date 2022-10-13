from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from application.presentation import url_prefix, security, Unauthorized

floor_tag = Tag(name='floor', description='Floor API Endpoints')

api_floor = APIBlueprint(
    '/floor',
    __name__,
    url_prefix=url_prefix,
    abp_tags=[floor_tag],
    abp_security=security,
    abp_responses={"401": Unauthorized},
    doc_ui=True
)

from application.presentation.endpoints import floor_endpoints
