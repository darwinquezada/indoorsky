from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from application.presentation import url_prefix, security, Unauthorized

wifi_tag = Tag(name='Wi-Fi', description='Wi-Fi API Endpoints')

api_wifi = APIBlueprint(
    '/wifi',
    __name__,
    url_prefix=url_prefix,
    abp_tags=[wifi_tag],
    abp_security=security,
    abp_responses={"401": Unauthorized},
    doc_ui=True
)

from application.presentation.endpoints import wifi_endpoints
