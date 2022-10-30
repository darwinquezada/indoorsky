import json
import os
from pydoc import cli
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from application.data.datasource.wifi_datasource import IWifiDatasource
from flask import jsonify, abort, g
from application.core.exceptions.status_codes import (SuccessResponseCode, 
                                                      ConflictResponseCode, 
                                                      NotFoundResponseCode, 
                                                      InternalServerErrorResponseCode)

r = RethinkDB()

class WifiDatasourceImpl(IWifiDatasource):
    def __init__(self, database_name: str, table_name: str) -> None:
        self.database_name = database_name
        self.table_name = table_name
    
    def get_wifi_by_id(self, wifi_id: str) -> dict:
        try:
            print(wifi_id)
            wifi = r.db(self.database_name).table(self.table_name).get(wifi_id).to_json().run(g.rdb_conn)
            if wifi is None or wifi=='null':
                return NotFoundResponseCode(message="Wi-Fi ID not found.")
            
            return json.loads(wifi)
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)
    
    def get_wifi_by_fingerprint_id(self, fingerprint_id: str) -> dict:
        try:
            wifis = r.db(self.database_name).table(self.table_name).filter({"fingerprint_id": fingerprint_id}).run(g.rdb_conn)
            if wifis==None:
                return NotFoundResponseCode(message="Fingerprint ID not found.")
            
            list_wifis = []
            for wifi in wifis:
                list_wifis.append(wifi)
                
            if not list_wifis:
                return NotFoundResponseCode()
            
            return jsonify(list_wifis)
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)  
        
    def insert_wifi(self, data: json) -> dict:
        try:

            insert = r.db(self.database_name).table(self.table_name).insert(data).run(g.rdb_conn)
            return SuccessResponseCode()
            
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)
    
    def delete_wifi_by_id(self, wifi_id: str) -> dict:
        try:
            wifi = r.db(self.database_name).table(self.table_name).get(wifi_id).delete().run(g.rdb_conn)
            if wifi['deleted'] == 0:
                return NotFoundResponseCode(message="Wi-Fi ID not found.")
            else:    
                return SuccessResponseCode()
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)
    
    def delete_wifi_by_fingerprint_id(self, fingerprint_id: str) -> dict:
        try:
            fingerprit = r.db(self.database_name).table(self.table_name).filter({'fingerprint_id': fingerprint_id}).delete().run(g.rdb_conn)
            if fingerprit['deleted'] == 0:
                return NotFoundResponseCode(message="Fingerprint ID not found")
            else:    
                return SuccessResponseCode()
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)