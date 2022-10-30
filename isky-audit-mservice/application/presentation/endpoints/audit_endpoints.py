import os
from pydoc import cli
import ssl
import json
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from flask import g, abort, Response, jsonify
from werkzeug.exceptions import HTTPException

from . import audit_tag, api_audit
from werkzeug.exceptions import (HTTPException, MethodNotAllowed, NotFound)
from application.core.exceptions.status_codes import (MethodNotAllowedResponseCode,NotFoundResponseCode)
from application.core.decorators.jwt_manager import login_required
from application.domain.entity.audit_entity import AuditEntity
from application.presentation.data_injection.injection_container import ApplicationContainer

# Environment request body
from application.presentation.req_body.audit_body import (AuditBody, AuditByUserIdBody)
# Use cases
from application.domain.use_cases.insert_audit_use_case import InsertAuditUseCase
from application.domain.use_cases.get_audit_by_user_id_use_case import GetAuditByUserIdUseCase

dotenv_path = os.path.join(os.getcwd(), '.env')
# Loading environment variables
if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)

# DB Instantiation
r = RethinkDB()

@api_audit.before_request
def before_request():
    try:
        # Database connection
        g.rdb_conn = r.connect(host=os.environ['RDB_HOST'], port=os.environ['RDB_PORT'], 
                               user=os.environ['RDB_USER'],
                               password=os.environ['RDB_PASSWORD'])
    except RqlDriverError as e:
        abort(Response(jsonify({'code':503, 'message': e.message})))

@api_audit.teardown_request
def teardown_request(exception):
    try:
        # Close the database connection
        g.rdb_conn.closse()
    except AttributeError:
        pass

@api_audit.errorhandler(NotFound)
def handle_exception(e):
    return NotFoundResponseCode()

@api_audit.errorhandler(MethodNotAllowed)
def handle_no_found():
    return MethodNotAllowedResponseCode()

@api_audit.errorhandler(404)
def page_not_found(e):
    return NotFoundResponseCode()

@api_audit.post('/audit', tags=[audit_tag])
@login_required
def insert_audit(body: AuditBody):
    insert_audit_use_case = InsertAuditUseCase(audit_repository=ApplicationContainer.audit_repository())
    data = {
        "user_id": body.user_id,
        "local_ip": body.local_ip,
        "external_ip": body.external_ip,
        "event": body.event,
        "description": body.description
        }
    return insert_audit_use_case.execute(data)

@api_audit.get('/audit/<user_id>', tags=[audit_tag])
@login_required
def get_audit_by_user_id(path: AuditByUserIdBody):
    # Get audit log by user ID
    get_audit_by_user_id_use_case = GetAuditByUserIdUseCase(audit_repository=ApplicationContainer.audit_repository())
    return get_audit_by_user_id_use_case.execute(user_id=path.user_id)
