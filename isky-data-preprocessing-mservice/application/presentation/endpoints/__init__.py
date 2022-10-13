from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from application.presentation import url_prefix, security, Unauthorized

preprocessing_tag = Tag(name='Preprocessing', description='Preprocessing API Endpoints')

api_preprocessing = APIBlueprint(
    '/preprocessing',
    __name__,
    url_prefix=url_prefix,
    abp_tags=[preprocessing_tag],
    abp_security=security,
    abp_responses={"401": Unauthorized},
    doc_ui=True
)

from application.presentation.endpoints import preprocessing_endpoints
