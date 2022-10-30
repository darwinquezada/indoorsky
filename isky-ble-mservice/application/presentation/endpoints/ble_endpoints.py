import os
from pydoc import cli
from dotenv import load_dotenv
from application.core.decorators.jwt_manager import login_required
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

from . import ble_tag, api_ble
from application.domain.entity.ble_entity import BleEntity
from application.presentation.data_injection.injection_container import ApplicationContainer
from flask import jsonify, g, abort
# ble request body
from application.presentation.req_body.ble_body import (BleFingerprintIdBody, BleIdBody)
# Use cases
from application.domain.use_cases.insert_ble_use_case import InsertbleUseCase
from application.domain.use_cases.get_ble_by_id_use_case import GetBleByIdUseCase
from application.domain.use_cases.get_ble_by_fingerprint_id_use_case import GetBleByFingerprintIdUseCase
from application.domain.use_cases.delete_ble_by_id_use_case import DeleteBleByIdUseCase
from application.domain.use_cases.delete_ble_by_fingerprint_id_use_case import DeleteBleByFingerprintIdUseCase

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)

r = RethinkDB()

@api_ble.before_request
def before_request():
    try:
        g.rdb_conn = r.connect(host=os.environ['RDB_HOST'], port=os.environ['RDB_PORT'], 
                               user=os.environ['RDB_USER'],
                               password=os.environ['RDB_PASSWORD'])
    except RqlDriverError:
        abort(503, "No database g.rdb_connection could be established.")

@api_ble.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.closse()
    except AttributeError:
        pass

@api_ble.post('/ble', tags=[ble_tag])
@login_required
def insert_ble(body: BleEntity):
        insert_ble_use_case = InsertbleUseCase(ble_repository=ApplicationContainer.ble_repository())
        data = {
                'fingerprint_id': body.fingerprint_id,
                'device_id': body.device_id,
                'name': body.name,
                'rssi': body.rssi
                }
        return insert_ble_use_case.execute(data)

@api_ble.get('/ble/<ble_id>', tags=[ble_tag])
@login_required
def get_ble_by_id(path: BleIdBody):
        get_ble_by_id_use_case = GetBleByIdUseCase(ble_repository=ApplicationContainer.ble_repository())
        return get_ble_by_id_use_case.execute(ble_id=path.ble_id)

@api_ble.get('/ble/<fingerprint_id>/fingerprint', tags=[ble_tag])
@login_required
def get_ble_by_fingerprint_id(path: BleFingerprintIdBody):
        get_ble_by_fingerprint_id_use_case = GetBleByFingerprintIdUseCase(ble_repository=ApplicationContainer.ble_repository())
        return get_ble_by_fingerprint_id_use_case.execute(fingerprint_id=path.fingerprint_id)

@api_ble.delete('/ble/<ble_id>/delete', tags=[ble_tag])
@login_required
def delete_ble_by_id(path: BleIdBody):
        delete_ble_by_id_use_case = DeleteBleByIdUseCase(ble_repository=ApplicationContainer.ble_repository())
        return delete_ble_by_id_use_case.execute(ble_id=path.ble_id)

@api_ble.delete('/ble/fingerprint/<fingerprint_id>/delete', tags=[ble_tag])
@login_required
def delete_ble_by_fingerprint_id(path:BleFingerprintIdBody):
        delete_ble_by_fingerprint = DeleteBleByFingerprintIdUseCase(ble_repository=ApplicationContainer.ble_repository())
        return delete_ble_by_fingerprint.execute(fingerprint_id=path.fingerprint_id)