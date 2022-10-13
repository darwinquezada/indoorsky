import json
import os
from pydoc import cli
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from application.data.datasource.environment_datasource import IEnvironmentDatasource
from flask import jsonify, abort, g

r = RethinkDB()

class EnvironmentDatasourceImpl(IEnvironmentDatasource):
    
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
                r.db(self.database_name).table(self.table_name).index_create("name").run(g.rdb_conn)
                r.db(self.database_name).table(self.table_name).index_wait("name").run(g.rdb_conn)

                pass
        except RqlRuntimeError as e:
            return jsonify({'code': '0', 'message': e.message})

    
    def create_environment(self, data: json) -> dict:
        try:
            self.verify_db()
            self.verify_table()
            
            filter_predicate = {
                "name": data['name']
            }
            
            reg_exist = r.db(self.database_name).table(self.table_name).filter(filter_predicate).count().eq(0).run(g.rdb_conn)
            
            if reg_exist == True:
                insert = r.db(self.database_name).table(self.table_name).insert(data).run(g.rdb_conn)
                return jsonify({'code':200, 'message':'Success!'})
            else:
                return jsonify({'code':409, 'message':'Oops ... you\'re trying to create an already existing record.'})
            
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})
    
    def get_environments(self) -> dict:
        try:
            self.verify_db()
            self.verify_table()
            environments = r.db(self.database_name).table(self.table_name).run(g.rdb_conn)
            
            if environments=='null':
                return jsonify({'code':204, 'message':'Oops ... No content'})
            
            list_environments = []
            
            for environment in environments:
                list_environments.append(environment)
            
            if not list_environments:
                return jsonify({'code':204, 'message':'Oops ... No content'})
            
            return jsonify(list_environments)
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e})
        
    def get_environment_by_id(self, env_id: str) -> dict:
        try:
            self.verify_db()
            self.verify_table()
            environment = r.db(self.database_name).table(self.table_name).get(env_id).to_json().run(g.rdb_conn)
            
            if environment=='null':
                return jsonify({'code':204, 'message':'Oops ... No content'})
            
            return json.loads(environment)
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e})
        
    def get_environment_by_name(self, name: str) -> dict:
        try:
            self.verify_db()
            self.verify_table()
            
            environments = r.db(self.database_name).table(self.table_name).filter({"name": name}).run(g.rdb_conn)
            if environments=='null':
                return jsonify({'code':204, 'message':'Oops ... No content'})
            
            list_environments = []
            for environment in environments:
                list_environments.append(environment)
                
            if not list_environments:
                return jsonify({'code':204, 'message':'Oops ... No content'})
            
            return jsonify(list_environments)
        except RuntimeError as e:
            return jsonify({'code':501, 'message':e.args})
            
    
    def delete_environment(self, env_id: str) -> dict:
        try:
            self.verify_db()
            self.verify_table()
            
            environment = r.db(self.database_name).table(self.table_name).get(env_id).delete().run(g.rdb_conn)
            if environment['deleted'] == 0:
                return jsonify({'code':400, 'message':'The id is invalid. This can happen if the item represented by the id has been deleted.'})
            else:    
                return jsonify({'code':200, 'message':'Success!'})
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})
    
    def update_environment(self, env_id: str, name: str, address: str, 
                           num_buildings: int, is_public: bool, 
                           is_active: bool) -> dict:
        try:
            self.verify_db()
            self.verify_table()
            environment = r.db(self.database_name).table(self.table_name).get(env_id).update({
                                                                    "name": name,
                                                                    "address": address,
                                                                    "num_buildings": num_buildings,
                                                                    "is_public": is_public,
                                                                    "is_active": is_active
                                                                }).run(g.rdb_conn)
            if environment['replaced'] == 0:
                return jsonify({'code':400, 'message':'The id is invalid. This can happen if the item represented by the id has been deleted.'})
            else:    
                return jsonify({'code':200, 'message':'Success!'})
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})