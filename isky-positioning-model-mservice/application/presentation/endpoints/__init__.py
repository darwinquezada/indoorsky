from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from application.presentation import url_prefix, security, Unauthorized

model_tag = Tag(name='Models and Algorithms', description='Models API Endpoints')

api_model = APIBlueprint(
    '/model',
    __name__,
    url_prefix=url_prefix,
    abp_tags=[model_tag],
    abp_security=security,
    abp_responses={"401": Unauthorized},
    doc_ui=True
)

from application.presentation.endpoints import model_endpoints
