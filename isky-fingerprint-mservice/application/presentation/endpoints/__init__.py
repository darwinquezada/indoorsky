from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from application.presentation import url_prefix, security, Unauthorized

fingerprint_tag = Tag(name='fingerprint', description='Fingerprint API Endpoints')

api_fingerprint = APIBlueprint(
    '/fingerprint',
    __name__,
    url_prefix=url_prefix,
    abp_tags=[fingerprint_tag],
    abp_security=security,
    abp_responses={"401": Unauthorized},
    doc_ui=True
)

from application.presentation.endpoints import fingerprint_endpoints
