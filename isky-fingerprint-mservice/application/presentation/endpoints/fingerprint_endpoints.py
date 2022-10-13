import os
from pydoc import cli
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

from . import fingerprint_tag, api_fingerprint
# from application.core.decorators.jwt_manager import login_required
from application.domain.entity.fingerprint_entity import FingerprintEntity
from application.presentation.data_injection.injection_container import ApplicationContainer

# Environment request body
from application.presentation.req_body.fingerprint_body import (FingerprintIdBody, FingerprintEnvBody, 
                                                                FingerprintBuildingBody, FingerprintFloorBody, 
                                                                FingerprintPoiBody)
# Use cases
from application.domain.use_cases.insert_fingerprint_use_case import InsertFingerprintUseCase
from application.domain.use_cases.get_fingerprint_by_id_use_case import GetFingerprintByIdUseCase
from application.domain.use_cases.get_fingerprint_by_field_use_case import GetFingerprintByFieldUseCase
from application.domain.use_cases.delete_fingerprint_by_id_use_case import DeleteFingerprintByIdUseCase
from application.domain.use_cases.delete_fingerprint_by_field_use_case import DeleteFingerprintByFieldUseCase
from flask import g, abort

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)

r = RethinkDB()

@api_fingerprint.before_request
def before_request():
    try:
        g.rdb_conn = r.connect(host=os.environ['RDB_HOST'], 
                           port=os.environ['RDB_PORT'])
    except RqlDriverError:
        abort(503, "No database g.rdb_connection could be established.")

@api_fingerprint.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.closse()
    except AttributeError:
        pass

@api_fingerprint.post('/fingerprint', tags=[fingerprint_tag])
# @login_required
def insert_fingerprint(body: FingerprintEntity):
        insert_fingerprint_use_case = InsertFingerprintUseCase(fingerprint_repository=ApplicationContainer.fingerprint_repository())
        data = {
                'id': body.id,
                'user_device': body.user_device,
                'os': body.os,
                'version': body.version,
                'env_id': body.env_id,
                'building_id': body.building_id,
                'floor_id': body.floor_id,
                'poi_id': body.poi_id
                }
        return insert_fingerprint_use_case.execute(data)

@api_fingerprint.get('/fingerprint/<fingerprint_id>', tags=[fingerprint_tag])
# @login_required
def get_fingerprint_by_id(path: FingerprintIdBody):
        get_fingerprint_by_id_use_case = GetFingerprintByIdUseCase(fingerprint_repository=ApplicationContainer.fingerprint_repository())
        return get_fingerprint_by_id_use_case.execute(fp_id=path.fingerprint_id)

@api_fingerprint.get('/fingerprint/<env_id>/environment', tags=[fingerprint_tag])
# @login_required
def get_fingerprint_by_env(path: FingerprintEnvBody):
        get_fingerprint_by_field_use_case = GetFingerprintByFieldUseCase(fingerprint_repository=ApplicationContainer.fingerprint_repository())
        return get_fingerprint_by_field_use_case.execute(field='env_id', value=path.env_id)

@api_fingerprint.get('/fingerprint/<building_id>/building', tags=[fingerprint_tag])
# @login_required
def get_fingerprint_by_building(path: FingerprintBuildingBody):
        get_fingerprint_by_field_use_case = GetFingerprintByFieldUseCase(fingerprint_repository=ApplicationContainer.fingerprint_repository())
        return get_fingerprint_by_field_use_case.execute(field='building_id', value=path.building_id)

@api_fingerprint.get('/fingerprint/<floor_id>/floor', tags=[fingerprint_tag])
# @login_required
def get_fingerprint_by_floor(path: FingerprintFloorBody):
        get_fingerprint_by_field_use_case = GetFingerprintByFieldUseCase(fingerprint_repository=ApplicationContainer.fingerprint_repository())
        return get_fingerprint_by_field_use_case.execute(field='floor_id', value=path.floor_id)

@api_fingerprint.get('/fingerprint/<poi_id>/poi', tags=[fingerprint_tag])
# @login_required
def get_fingerprint_by_poi(path: FingerprintPoiBody):
        get_fingerprint_by_field_use_case = GetFingerprintByFieldUseCase(fingerprint_repository=ApplicationContainer.fingerprint_repository())
        return get_fingerprint_by_field_use_case.execute(field='poi_id', value=path.poi_id)

@api_fingerprint.delete('/fingerprint/<fingerprint_id>/delete', tags=[fingerprint_tag])
# @login_required
def delete_fingerprint_by_id(path: FingerprintIdBody):
        delete_fingerprint_by_id_use_case = DeleteFingerprintByIdUseCase(fingerprint_repository=ApplicationContainer.fingerprint_repository())
        return delete_fingerprint_by_id_use_case.execute(fp_id=path.fingerprint_id)

@api_fingerprint.delete('/fingerprint/<env_id>/environment/delete', tags=[fingerprint_tag])
# @login_required
def delete_fingerprint_by_env(path: FingerprintEnvBody):
        delete_fingerprint_by_field_use_case = DeleteFingerprintByFieldUseCase(fingerprint_repository=ApplicationContainer.fingerprint_repository())
        return delete_fingerprint_by_field_use_case.execute(field='env_id', value=path.env_id)

@api_fingerprint.delete('/fingerprint/<building_id>/building/delete', tags=[fingerprint_tag])
# @login_required
def delete_fingerprint_by_building(path: FingerprintBuildingBody):
        delete_fingerprint_by_field_use_case = DeleteFingerprintByFieldUseCase(fingerprint_repository=ApplicationContainer.fingerprint_repository())
        return delete_fingerprint_by_field_use_case.execute(field='building_id', value=path.building_id)

@api_fingerprint.delete('/fingerprint/<floor_id>/floor/delete', tags=[fingerprint_tag])
# @login_required
def delete_fingerprint_by_floor(path: FingerprintFloorBody):
        delete_fingerprint_by_field_use_case = DeleteFingerprintByFieldUseCase(fingerprint_repository=ApplicationContainer.fingerprint_repository())
        return delete_fingerprint_by_field_use_case.execute(field='floor_id', value=path.floor_id)

@api_fingerprint.delete('/fingerprint/<poi_id>/poi/delete', tags=[fingerprint_tag])
# @login_required
def delete_fingerprint_by_poi(path: FingerprintPoiBody):
        delete_fingerprint_by_field_use_case = DeleteFingerprintByFieldUseCase(fingerprint_repository=ApplicationContainer.fingerprint_repository())
        return delete_fingerprint_by_field_use_case.execute(field='poi_id', value=path.poi_id)