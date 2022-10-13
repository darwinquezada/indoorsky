import os
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from . import environment_tag, api_environment
from application.core.decorators.jwt_manager import login_required
from application.data.model.environment_model import EnvironmentModel
from application.domain.entity.environment_entity import EnvironmentEntity
from application.presentation.data_injection.injection_container import ApplicationContainer
from flask import jsonify,g, abort
# Environment request body
from application.presentation.req_body.environment_body import (EnvironmentBody, EnvironmentId, EnvironmentName)
# Use cases
from application.domain.use_cases.create_environment_use_case import CreateEnvironmentUseCase
from application.domain.use_cases.get_environment_by_id_use_case import GetEnvironmentByIdUseCase
from application.domain.use_cases.get_environment_by_name_use_case import GetEnvironmentByNameUseCase
from application.domain.use_cases.update_environment_use_case import UpdateEnvironmentUseCase
from application.domain.use_cases.delete_environment_use_case import DeleteEnvironmentUseCase
from application.domain.use_cases.get_environments_use_case import GetEnvironmentsUseCase

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)

r = RethinkDB()

@api_environment.before_request
def before_request():
    try:
        g.rdb_conn = r.connect(host=os.environ['RDB_HOST'], 
                           port=os.environ['RDB_PORT'])
    except RqlDriverError:
        abort(503, "No database g.rdb_connection could be established.")

@api_environment.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.closse()
    except AttributeError:
        pass

@api_environment.post('/environment', tags=[environment_tag])
# @login_required
def insert_environment(body: EnvironmentEntity):
        insert_environment_use_case = CreateEnvironmentUseCase(environment_repository=ApplicationContainer.environment_repository())
        data = {
                "name": body.name,
                "address": body.address,
                "num_buildings": body.num_buildings,
                "is_public": body.is_public,
                "is_active": body.is_active}
        return insert_environment_use_case.execute(data)

@api_environment.get('/environment', tags=[environment_tag])
# @login_required
def get_environments():
        get_environments_use_case = GetEnvironmentsUseCase(environment_repository=ApplicationContainer.environment_repository())
        return get_environments_use_case.execute()

@api_environment.get('/environment/<env_id>', tags=[environment_tag])
# @login_required
def get_environment_by_id(path: EnvironmentId):
        get_environment_use_case = GetEnvironmentByIdUseCase(environment_repository=ApplicationContainer.environment_repository())
        return get_environment_use_case.execute(env_id=path.env_id)

@api_environment.get('/environment/<name>/name', tags=[environment_tag])
# @login_required
def get_environment_by_name(path: EnvironmentName):
        get_environment_use_case = GetEnvironmentByNameUseCase(environment_repository=ApplicationContainer.environment_repository())
        return get_environment_use_case.execute(name=path.name)

@api_environment.delete('/environment/<env_id>/delete', tags=[environment_tag])
# @login_required
def delete_environment_by_id(path: EnvironmentId):
        delete_environment_use_case = DeleteEnvironmentUseCase(environment_repository=ApplicationContainer.environment_repository())
        return delete_environment_use_case.execute(env_id=path.env_id)

@api_environment.put('/environment/<env_id>/update', tags=[environment_tag])
# @login_required
def update_environment(path:EnvironmentId, body:EnvironmentEntity):
        update_environment_use_case = UpdateEnvironmentUseCase(environment_repository=ApplicationContainer.environment_repository())
        return update_environment_use_case.execute( env_id=path.env_id, name=body.name, address=body.address,
                                               num_buildings=body.num_buildings,
                                               is_public=body.is_public, is_active=body.is_active)