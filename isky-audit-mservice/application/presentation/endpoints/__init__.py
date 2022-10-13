from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from application.presentation import url_prefix, security, Unauthorized

audit_tag = Tag(name='Audit', description='Audit API Endpoints')

api_audit = APIBlueprint(
    '/audit',
    __name__,
    url_prefix=url_prefix,
    abp_tags=[audit_tag],
    abp_security=security,
    abp_responses={"401": Unauthorized},
    doc_ui=True
)

from application.presentation.endpoints import audit_endpoints
