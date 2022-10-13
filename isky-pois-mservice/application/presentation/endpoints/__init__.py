from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from application.presentation import url_prefix, security, Unauthorized

poi_tag = Tag(name='POI', description='POI API Endpoints')

api_poi = APIBlueprint(
    '/poi',
    __name__,
    url_prefix=url_prefix,
    abp_tags=[poi_tag],
    abp_security=security,
    abp_responses={"401": Unauthorized},
    doc_ui=True
)

from application.presentation.endpoints import poi_endpoints
