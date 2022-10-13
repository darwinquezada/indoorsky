import json
import os
from pydoc import cli
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from application.data.datasource.audit_datasource import IAuditDatasource
from flask import jsonify, abort, g
from application.core.exceptions.status_codes import CreateSuccessCode, DeleteSuccessCode

r = RethinkDB()

class AuditDatasourceImpl(IAuditDatasource):
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
            
            list_indexes = r.db(self.database_name).table(self.table_name).index_list().run(g.rdb_conn)
            
            if not list_indexes :
                r.db(self.database_name).table(self.table_name).index_create("user_id").run(g.rdb_conn)
                r.db(self.database_name).table(self.table_name).index_wait("user_id").run(g.rdb_conn)

                pass
        except RqlRuntimeError as e:
            return jsonify({'code': '0', 'message': e.message})
        
    def insert_audit(self, data: json) -> dict:
        try:
            self.verify_db()
            self.verify_table()
            
            filter_predicate = {
                "user_id": data['user_id'],
                "local_ip": data['local_ip'],
                "external_ip": data['external_ip'],
                "event": data['event'],
                "description": data['description']
            }
            
            reg_exist = r.db(self.database_name).table(self.table_name).filter(filter_predicate).count().eq(0).run(g.rdb_conn)
            
            if reg_exist == True:
                insert = r.db(self.database_name).table(self.table_name).insert(data).run(g.rdb_conn)
                return jsonify({'code':200, 'message':'Success!'})
            else:
                return jsonify({'code':409, 'message':'Oops ... you\'re trying to create an already existing record.'})
            
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})
    
    def get_audit_by_user_id(self, user_id: str) -> dict:
        try:
            audit = r.db(self.database_name).table(self.table_name).filter({"user_id": user_id}).run(g.rdb_conn)
            if audit==None:
                return jsonify({'code':204, 'message':'Oops ... No content'})
            
            return json.loads(audit)
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e})
    
   