from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from application.presentation import url_prefix, security, Unauthorized

ble_tag = Tag(name='BLE', description='BLE API Endpoints')

api_ble = APIBlueprint(
    '/ble',
    __name__,
    url_prefix=url_prefix,
    abp_tags=[ble_tag],
    abp_security=security,
    abp_responses={"401": Unauthorized},
    doc_ui=True
)

from application.presentation.endpoints import ble_endpoints
