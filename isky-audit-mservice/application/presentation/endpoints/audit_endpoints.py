import os
from pydoc import cli
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from flask import g, abort

from . import audit_tag, api_audit
from application.core.decorators.jwt_manager import login_required
from application.domain.entity.audit_entity import AuditEntity
from application.presentation.data_injection.injection_container import ApplicationContainer

# Environment request body
from application.presentation.req_body.audit_body import (AuditBody, AuditByUserIdBody)
# Use cases
from application.domain.use_cases.insert_audit_use_case import InsertAuditUseCase
from application.domain.use_cases.get_audit_by_user_id_use_case import GetAuditByUserIdUseCase

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)

r = RethinkDB()

@api_audit.before_request
def before_request():
    try:
        g.rdb_conn = r.connect(host=os.environ['RDB_HOST'], 
                           port=os.environ['RDB_PORT'])
    except RqlDriverError:
        abort(503, "No database g.rdb_connection could be established.")

@api_audit.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.closse()
    except AttributeError:
        pass

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
        get_audit_by_user_id_use_case = GetAuditByUserIdUseCase(audit_repository=ApplicationContainer.audit_repository())
        return get_audit_by_user_id_use_case.execute(user_id=path.user_id)
