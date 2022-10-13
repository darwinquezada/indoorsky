import json
import os
from pydoc import cli
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from application.data.datasource.fingerprint_datasource import IFingerprintDatasource
from flask import jsonify, abort, g
import time
from datetime import datetime

r = RethinkDB()

class FingerprintDatasourceImpl(IFingerprintDatasource):
    def __init__(self, database_name: str, table_name: str) -> None:
        self.database_name = database_name
        self.table_name = table_name
        
    def verify_db(self) -> dict:
        try:
            list_databases = r.db_list().run(g.rdb_conn)
            
            if not self.database_name in list_databases:
                r.db_create(self.database_name).run(g.rdb_conn)
                r.db(self.database_name).table_create(self.table_name).run(g.rdb_conn)
                pass
        except RqlRuntimeError as e:
            return jsonify({'code': '0', 'message': e.message})

    def verify_table(self) -> dict:
        try:
            list_tables = r.db(self.database_name).table_list().run(g.rdb_conn)
            if not self.table_name in list_tables:
                r.db(self.database_name).table_create(self.table_name).run(g.rdb_conn)
                pass
            
        except RqlRuntimeError as e:
            return jsonify({'code': '0', 'message': e.message})
    
    def insert_fingerprint(self, data: json) -> dict:
        try:
            self.verify_db()
            self.verify_table()
            
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
            return jsonify({'code':200, 'message':'Success!'})
        
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})
    
    def get_fingerprint_by_id(self, fp_id: str) -> dict:
        try:
            fingerprint = r.db(self.database_name).table(self.table_name).get(fp_id).to_json().run(g.rdb_conn)
            if fingerprint==None:
                return jsonify({'code':204, 'message':'Oops ... No content'})
            
            return json.loads(fingerprint)
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e})
    
    def delete_fingerprint_by_id(self, fp_id: str) -> dict:
        try:
            fingerprit = r.db(self.database_name).table(self.table_name).get(fp_id).delete().run(g.rdb_conn)
            if fingerprit['deleted'] == 0:
                return jsonify({'code':400, 'message':'The id is invalid. This can happen if the item represented by the id has been deleted.'})
            else:    
                return jsonify({'code':200, 'message':'Success!'})
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})
    
    def get_fingerprint_by_field(self, field: str, value: str) -> dict:
        try:
            fingerprints = r.db(self.database_name).table(self.table_name).filter({ field: value }).run(g.rdb_conn)
            if fingerprints==None:
                return jsonify({'code':204, 'message':'Oops ... No content'})
            
            list_fingerprints = []
            for fingerprint in fingerprints:
                list_fingerprints.append(fingerprint)
                
            if not list_fingerprints:
                return jsonify({'code':204, 'message':'Oops ... No content'})
            
            return jsonify(list_fingerprints)
        except RuntimeError as e:
            return jsonify({'code':501, 'message':e.args})
        
    def delete_fingerprint_by_field(self, field: str, value: str) -> dict:
        try:
            fingerprit = r.db(self.database_name).table(self.table_name).filter({field: value}).delete().run(g.rdb_conn)
            if fingerprit['deleted'] == 0:
                return jsonify({'code':400, 'message':'The id is invalid. This can happen if the item represented by the id has been deleted.'})
            else:    
                return jsonify({'code':200, 'message':'Success!'})
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})