import json
import os
from pydoc import cli
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from application.data.datasource.ble_datasource import IBleDatasource
from flask import jsonify, abort, g
from application.core.exceptions.status_codes import CreateSuccessCode, DeleteSuccessCode
 
r = RethinkDB()

class BleDatasourceImpl(IBleDatasource):
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
    
    def get_ble_by_id(self, ble_id: str) -> dict:
        try:
            print(ble_id)
            ble = r.db(self.database_name).table(self.table_name).get(ble_id).to_json().run(g.rdb_conn)
            if ble is None or ble=='null':
                return jsonify({'code':204, 'message':'Oops ... No content'})
            
            return json.loads(ble)
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e})
    
    def get_ble_by_fingerprint_id(self, fingerprint_id: str) -> dict:
        try:
            bles = r.db(self.database_name).table(self.table_name).filter({"fingerprint_id": fingerprint_id}).run(g.rdb_conn)
            if bles==None:
                return jsonify({'code':204, 'message':'Oops ... No content'})
            
            list_bles = []
            for ble in bles:
                list_bles.append(ble)
                
            if not list_bles:
                return jsonify({'code':204, 'message':'Oops ... No content'})
            
            return jsonify(list_bles)
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})  
        
    def insert_ble(self, data: json) -> dict:
        try:
            self.verify_db()
            self.verify_table()

            insert = r.db(self.database_name).table(self.table_name).insert(data).run(g.rdb_conn)
            return jsonify({'code':200, 'message':'Success!'})
            
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})
    
    def delete_ble_by_id(self, ble_id: str) -> dict:
        try:
            ble = r.db(self.database_name).table(self.table_name).get(ble_id).delete().run(g.rdb_conn)
            if ble['deleted'] == 0:
                return jsonify({'code':400, 'message':'The id is invalid. This can happen if the item represented by the id has been deleted.'})
            else:    
                return jsonify({'code':200, 'message':'Success!'})
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})
    
    def delete_ble_by_fingerprint_id(self, fingerprint_id: str) -> dict:
        try:
            fingerprit = r.db(self.database_name).table(self.table_name).filter({'fingerprint_id': fingerprint_id}).delete().run(g.rdb_conn)
            if fingerprit['deleted'] == 0:
                return jsonify({'code':400, 'message':'The id is invalid. This can happen if the item represented by the id has been deleted.'})
            else:    
                return jsonify({'code':200, 'message':'Success!'})
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})