import os
from pydoc import cli
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

from . import wifi_tag, api_wifi
from application.domain.entity.wifi_entity import WifiEntity
from application.presentation.data_injection.injection_container import ApplicationContainer
from flask import jsonify, g, abort
# wifi request body
from application.presentation.req_body.wifi_body import (WifiFingerprintIdBody, WifiIdBody)
# Use cases
from application.domain.use_cases.insert_wifi_use_case import InsertWifiUseCase
from application.domain.use_cases.get_wifi_by_id_use_case import GetWifiByIdUseCase
from application.domain.use_cases.get_wifi_by_fingerprint_id_use_case import GetWifiByFingerprintIdUseCase
from application.domain.use_cases.delete_wifi_by_id_use_case import DeleteWifiByIdUseCase
from application.domain.use_cases.delete_wifi_by_fingerprint_id_use_case import DeleteWifiByFingerprintIdUseCase

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)

r = RethinkDB()

@api_wifi.before_request
def before_request():
    try:
        g.rdb_conn = r.connect(host=os.environ['RDB_HOST'], 
                           port=os.environ['RDB_PORT'])
    except RqlDriverError:
        abort(503, "No database g.rdb_connection could be established.")

@api_wifi.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.closse()
    except AttributeError:
        pass

@api_wifi.post('/wifi', tags=[wifi_tag])
# @login_required
def insert_wifi(body: WifiEntity):
        insert_wifi_use_case = InsertWifiUseCase(wifi_repository=ApplicationContainer.wifi_repository())
        data = {
                'fingerprint_id': body.fingerprint_id,
                'ssid': body.ssid,
                'bssid': body.bssid,
                'rssi': body.rssi
                }
        return insert_wifi_use_case.execute(data)

@api_wifi.get('/wifi/<wifi_id>', tags=[wifi_tag])
# @login_required
def get_wifi_by_id(path: WifiIdBody):
        get_wifi_by_id_use_case = GetWifiByIdUseCase(wifi_repository=ApplicationContainer.wifi_repository())
        return get_wifi_by_id_use_case.execute(wifi_id=path.wifi_id)

@api_wifi.get('/wifi/<fingerprint_id>/fingerprint', tags=[wifi_tag])
# @login_required
def get_wifi_by_fingerprint_id(path: WifiFingerprintIdBody):
        get_wifi_by_fingerprint_id_use_case = GetWifiByFingerprintIdUseCase(wifi_repository=ApplicationContainer.wifi_repository())
        return get_wifi_by_fingerprint_id_use_case.execute(fingerprint_id=path.fingerprint_id)

@api_wifi.delete('/wifi/<wifi_id>/delete', tags=[wifi_tag])
# @login_required
def delete_wifi_by_id(path: WifiIdBody):
        delete_wifi_by_id_use_case = DeleteWifiByIdUseCase(wifi_repository=ApplicationContainer.wifi_repository())
        return delete_wifi_by_id_use_case.execute(wifi_id=path.wifi_id)

@api_wifi.delete('/wifi/fingerprint/<fingerprint_id>/delete', tags=[wifi_tag])
# @login_required
def delete_wifi_by_fingerprint_id(path:WifiFingerprintIdBody):
        delete_wifi_by_fingerprint = DeleteWifiByFingerprintIdUseCase(wifi_repository=ApplicationContainer.wifi_repository())
        return delete_wifi_by_fingerprint.execute(fingerprint_id=path.fingerprint_id)