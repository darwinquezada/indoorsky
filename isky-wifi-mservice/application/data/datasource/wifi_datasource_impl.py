import json
import os
from pydoc import cli
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from application.data.datasource.wifi_datasource import IWifiDatasource
from flask import jsonify, abort, g
from application.core.exceptions.status_codes import CreateSuccessCode, DeleteSuccessCode
 
r = RethinkDB()

class WifiDatasourceImpl(IWifiDatasource):
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
    
    def get_wifi_by_id(self, wifi_id: str) -> dict:
        try:
            print(wifi_id)
            wifi = r.db(self.database_name).table(self.table_name).get(wifi_id).to_json().run(g.rdb_conn)
            if wifi is None or wifi=='null':
                return jsonify({'code':204, 'message':'Oops ... No content'})
            
            return json.loads(wifi)
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e})
    
    def get_wifi_by_fingerprint_id(self, fingerprint_id: str) -> dict:
        try:
            wifis = r.db(self.database_name).table(self.table_name).filter({"fingerprint_id": fingerprint_id}).run(g.rdb_conn)
            if wifis==None:
                return jsonify({'code':204, 'message':'Oops ... No content'})
            
            list_wifis = []
            for wifi in wifis:
                list_wifis.append(wifi)
                
            if not list_wifis:
                return jsonify({'code':204, 'message':'Oops ... No content'})
            
            return jsonify(list_wifis)
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})  
        
    def insert_wifi(self, data: json) -> dict:
        try:
            self.verify_db()
            self.verify_table()

            insert = r.db(self.database_name).table(self.table_name).insert(data).run(g.rdb_conn)
            return jsonify({'code':200, 'message':'Success!'})
            
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})
    
    def delete_wifi_by_id(self, wifi_id: str) -> dict:
        try:
            wifi = r.db(self.database_name).table(self.table_name).get(wifi_id).delete().run(g.rdb_conn)
            if wifi['deleted'] == 0:
                return jsonify({'code':400, 'message':'The id is invalid. This can happen if the item represented by the id has been deleted.'})
            else:    
                return jsonify({'code':200, 'message':'Success!'})
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})
    
    def delete_wifi_by_fingerprint_id(self, fingerprint_id: str) -> dict:
        try:
            fingerprit = r.db(self.database_name).table(self.table_name).filter({'fingerprint_id': fingerprint_id}).delete().run(g.rdb_conn)
            if fingerprit['deleted'] == 0:
                return jsonify({'code':400, 'message':'The id is invalid. This can happen if the item represented by the id has been deleted.'})
            else:    
                return jsonify({'code':200, 'message':'Success!'})
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})