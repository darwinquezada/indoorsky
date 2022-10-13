from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from application.presentation import url_prefix, security, Unauthorized

cleansing_tag = Tag(name='Data cleansing', description='Data cleansing API Endpoints')

api_cleansing = APIBlueprint(
    '/cleansing',
    __name__,
    url_prefix=url_prefix,
    abp_tags=[cleansing_tag],
    abp_security=security,
    abp_responses={"401": Unauthorized},
    doc_ui=True
)

from application.presentation.endpoints import cleansing_endpoints
