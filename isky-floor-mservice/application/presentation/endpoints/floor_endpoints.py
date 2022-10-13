import os
from pydoc import cli
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from flask import g, abort

from . import floor_tag, api_floor
# from application.core.decorators.jwt_manager import login_required
from application.domain.entity.floor_entity import FloorEntity
from application.presentation.data_injection.injection_container import ApplicationContainer

# Environment request body
from application.presentation.req_body.floor_body import (FloorIdBody, FloorLevelBody, FloorBody)
# Use cases
from application.domain.use_cases.insert_floor_use_case import InsertFloorUseCase
from application.domain.use_cases.get_floor_by_id_use_case import GetFloorByIdUseCase
from application.domain.use_cases.get_floor_by_level_use_case import GetFloorByLevelUseCase
from application.domain.use_cases.update_floor_use_case import UpdateFloorUseCase
from application.domain.use_cases.delete_floor_use_case import DeleteFloorUseCase

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)

r = RethinkDB()

@api_floor.before_request
def before_request():
    try:
        g.rdb_conn = r.connect(host=os.environ['RDB_HOST'], 
                           port=os.environ['RDB_PORT'])
    except RqlDriverError:
        abort(503, "No database g.rdb_connection could be established.")

@api_floor.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.closse()
    except AttributeError:
        pass

@api_floor.post('/floor', tags=[floor_tag])
# @login_required
def insert_floor(body: FloorEntity):
        insert_floor_use_case = InsertFloorUseCase(floor_repository=ApplicationContainer.floor_repository())
        data = {
                "building_id": body.building_id,
                "level": body.level,
                "is_public": body.is_public,
                "is_active": body.is_active
                }
        return insert_floor_use_case.execute(data)

@api_floor.get('/floor/<floor_id>', tags=[floor_tag])
# @login_required
def get_floor_by_id(path: FloorIdBody):
        get_floor_by_id_use_case = GetFloorByIdUseCase(floor_repository=ApplicationContainer.floor_repository())
        return get_floor_by_id_use_case.execute(floor_id=path.floor_id)

@api_floor.get('/floor/<level>/level', tags=[floor_tag])
# @login_required
def get_floor_by_level(path: FloorLevelBody):
        get_floor_by_level_use_case = GetFloorByLevelUseCase(floor_repository=ApplicationContainer.floor_repository())
        return get_floor_by_level_use_case.execute(level=path.level)

@api_floor.delete('/floor/<floor_id>/delete', tags=[floor_tag])
# @login_required
def delete_floor_by_id(path: FloorIdBody):
        delete_use_case = DeleteFloorUseCase(floor_repository=ApplicationContainer.floor_repository())
        return delete_use_case.execute(floor_id=path.floor_id)


@api_floor.put('/floor/<floor_id>/update', tags=[floor_tag])
# @login_required
def update_floor(path:FloorIdBody, body:FloorBody):
        update_floor_use_case = UpdateFloorUseCase(floor_repository=ApplicationContainer.floor_repository())
        return update_floor_use_case.execute(floor_id=path.floor_id, building_id=body.building_id,
                                                        level=body.level, is_public=body.is_public, 
                                                        is_active=body.is_active)