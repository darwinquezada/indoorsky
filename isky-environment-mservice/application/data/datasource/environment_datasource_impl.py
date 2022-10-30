import json
import os
from pydoc import cli
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from application.data.datasource.environment_datasource import IEnvironmentDatasource
from application.core.exceptions.status_codes import (SuccessResponseCode, NotFoundResponseCode, 
                                                      InternalServerErrorResponseCode, ConflictResponseCode)
from flask import jsonify, abort, g

r = RethinkDB()

class EnvironmentDatasourceImpl(IEnvironmentDatasource):
    
    def __init__(self, database_name: str, table_name: str) -> None:
        self.database_name = database_name
        self.table_name = table_name
    
    def create_environment(self, data: json) -> dict:
        try:
            
            filter_predicate = {
                "name": data['name']
            }
            
            reg_exist = r.db(self.database_name).table(self.table_name).filter(filter_predicate).count().eq(0).run(g.rdb_conn)
            
            if reg_exist == True:
                insert = r.db(self.database_name).table(self.table_name).insert(data).run(g.rdb_conn)
                return SuccessResponseCode()
            else:
                return ConflictResponseCode(message="There is a register with the same name.")
            
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)
    
    def get_environments(self) -> dict:
        try:
            environments = r.db(self.database_name).table(self.table_name).run(g.rdb_conn)
            
            if environments=='null':
                return NotFoundResponseCode(message="Environments not found.")
            
            list_environments = []
            
            for environment in environments:
                list_environments.append(environment)
            
            if not list_environments:
                return NotFoundResponseCode()
            
            return jsonify(list_environments)
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)
        
    def get_environment_by_id(self, env_id: str) -> dict:
        try:
            environment = r.db(self.database_name).table(self.table_name).get(env_id).to_json().run(g.rdb_conn)
            
            if environment=='null':
                return NotFoundResponseCode(message="Environment ID not found.")
            
            return json.loads(environment)
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)
        
    def get_environment_by_name(self, name: str) -> dict:
        try:
            environments = r.db(self.database_name).table(self.table_name).filter({"name": name}).run(g.rdb_conn)
            if environments=='null':
                return NotFoundResponseCode(message="Name not found.")
            
            list_environments = []
            for environment in environments:
                list_environments.append(environment)
                
            if not list_environments:
                return NotFoundResponseCode()
            
            return jsonify(list_environments)
        except RuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)
            
    
    def delete_environment(self, env_id: str) -> dict:
        try:
            environment = r.db(self.database_name).table(self.table_name).get(env_id).delete().run(g.rdb_conn)
            if environment['deleted'] == 0:
                return NotFoundResponseCode(message="Environment ID not found.")
            else:    
                return SuccessResponseCode()
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)
    
    def update_environment(self, env_id: str, name: str, address: str, 
                           num_buildings: int, is_public: bool, 
                           is_active: bool) -> dict:
        try:
            environment = r.db(self.database_name).table(self.table_name).get(env_id).update({
                                                                    "name": name,
                                                                    "address": address,
                                                                    "num_buildings": num_buildings,
                                                                    "is_public": is_public,
                                                                    "is_active": is_active
                                                                }).run(g.rdb_conn)
            if environment['replaced'] == 0:
                return NotFoundResponseCode(message="Environment ID not found.")
            else:    
                return SuccessResponseCode()
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)