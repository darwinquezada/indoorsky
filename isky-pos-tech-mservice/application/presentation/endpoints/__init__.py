from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from application.presentation import url_prefix, security, Unauthorized

pos_tech_tag = Tag(name='Positioning Technology', description='Positioning Technology API Endpoints')

api_pos_tech = APIBlueprint(
    '/pos_tech',
    __name__,
    url_prefix=url_prefix,
    abp_tags=[pos_tech_tag],
    abp_security=security,
    abp_responses={"401": Unauthorized},
    doc_ui=True
)

from application.presentation.endpoints import pos_tech_endpoints
