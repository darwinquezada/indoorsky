import json
import os
from pydoc import cli
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from application.data.datasource.fingerprint_datasource import IFingerprintDatasource
from application.core.exceptions.status_codes import (SuccessResponseCode, NotFoundResponseCode,
                                                      InternalServerErrorResponseCode, ConflictResponseCode)
from flask import jsonify, abort, g
import time
from datetime import datetime

r = RethinkDB()

class FingerprintDatasourceImpl(IFingerprintDatasource):
    def __init__(self, database_name: str, table_name: str) -> None:
        self.database_name = database_name
        self.table_name = table_name
    
    def insert_fingerprint(self, data: json) -> dict:
        try:
            
            millisecond = datetime.now()
            created= time.mktime(millisecond.timetuple()) * 1000
            
            insert_data = {
                'id': data['id'],
                'user_device': data['user_device'],
                'os': data['os'],
                'version': data['version'],
                'env_id': data['env_id'],
                'building_id': data['building_id'],
                'floor_id': data['floor_id'],
                'poi_id': data['poi_id'],
                'created_at': created,
                'updated_at': created
            }
      
            insert = r.db(self.database_name).table(self.table_name).insert(insert_data).run(g.rdb_conn)
            return SuccessResponseCode()
        
        except RqlRuntimeError as e:
            InternalServerErrorResponseCode(message=e.message)
    
    def get_fingerprint_by_id(self, fp_id: str) -> dict:
        try:
            fingerprint = r.db(self.database_name).table(self.table_name).get(fp_id).to_json().run(g.rdb_conn)
            if fingerprint==None:
                return NotFoundResponseCode(message="Fingerprint ID not found.")
            
            return json.loads(fingerprint)
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)
    
    def delete_fingerprint_by_id(self, fp_id: str) -> dict:
        try:
            fingerprit = r.db(self.database_name).table(self.table_name).get(fp_id).delete().run(g.rdb_conn)
            if fingerprit['deleted'] == 0:
                return NotFoundResponseCode(message="Fingerprint ID not found.")
            else:    
                return SuccessResponseCode()
        except RqlRuntimeError as e:
            InternalServerErrorResponseCode(message=e.message)
    
    def get_fingerprint_by_field(self, field: str, value: str) -> dict:
        try:
            fingerprints = r.db(self.database_name).table(self.table_name).filter({ field: value }).run(g.rdb_conn)
            if fingerprints==None:
                return NotFoundResponseCode(message= field + " not found.")
            
            list_fingerprints = []
            for fingerprint in fingerprints:
                list_fingerprints.append(fingerprint)
                
            if not list_fingerprints:
                return NotFoundResponseCode()
            
            return jsonify(list_fingerprints)
        except RuntimeError as e:
            InternalServerErrorResponseCode(message=e.message)
        
    def delete_fingerprint_by_field(self, field: str, value: str) -> dict:
        try:
            fingerprit = r.db(self.database_name).table(self.table_name).filter({field: value}).delete().run(g.rdb_conn)
            if fingerprit['deleted'] == 0:
                return NotFoundResponseCode(message= field + " not found.")
            else:    
                return SuccessResponseCode()
        except RqlRuntimeError as e:
            InternalServerErrorResponseCode(message=e.message)