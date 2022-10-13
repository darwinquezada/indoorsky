import json
import os
from pydoc import cli
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from application.data.datasource.building_datasource import IBuildingDatasource
from flask import jsonify, abort, g
from application.core.exceptions.status_codes import CreateSuccessCode, DeleteSuccessCode

r = RethinkDB()

class BuildingDatasourceImpl(IBuildingDatasource):
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
                r.db(self.database_name).table(self.table_name).index_create("env_id").run(g.rdb_conn)
                r.db(self.database_name).table(self.table_name).index_create("name").run(g.rdb_conn)
                r.db(self.database_name).table(self.table_name).index_wait("env_id").run(g.rdb_conn)
                r.db(self.database_name).table(self.table_name).index_wait("name").run(g.rdb_conn)
                
                pass
        except RqlRuntimeError as e:
            return jsonify({'code': '0', 'message': e.message})
        
    def insert_building(self, data: json) -> dict:
        try:
            self.verify_db()
            self.verify_table()
            
            filter_predicate = {
                "name": data['name'],
                "env_id": data['env_id']
            }
            
            reg_exist = r.db(self.database_name).table(self.table_name).filter(filter_predicate).count().eq(0).run(g.rdb_conn)
            
            if reg_exist == True:
                insert = r.db(self.database_name).table(self.table_name).insert(data).run(g.rdb_conn)
                return CreateSuccessCode()
            else:
                return jsonify({'code':409, 'message':'Oops ... you\'re trying to create an already existing record.'})
            
        except RuntimeError as e:
            return jsonify({'code':501, 'message':e.args})
    
    def get_building_by_id(self, building_id: str) -> dict:
        try:
            self.verify_db()
            self.verify_table()
            building = r.db(self.database_name).table(self.table_name).get(building_id).to_json().run(g.rdb_conn)
            if building=='null':
                return jsonify({'code':204, 'message':'Oops ... No content'})
            
            return json.loads(building)
        except RuntimeError as e:
            return jsonify({'code':501, 'message':e})
    
    def get_building_by_name(self, name: str) -> dict:
        try:
            self.verify_db()
            self.verify_table()
            buildings = r.db(self.database_name).table(self.table_name).filter({"name": name}).run(g.rdb_conn)
            if buildings=='null':
                return jsonify({'code':204, 'message':'Oops ... No content'})
            
            list_buildings = []
            for building in buildings:
                list_buildings.append(building)
                
            if not list_buildings:
                return jsonify({'code':204, 'message':'Oops ... No content'})
            
            return jsonify(list_buildings)
        except RuntimeError as e:
            return jsonify({'code':501, 'message':e.args})
    
    def delete_building(self, building_id: str) -> dict:
        try:
            self.verify_db()
            self.verify_table()
            building = r.db(self.database_name).table(self.table_name).get(building_id).delete().run(g.rdb_conn)
            if building['deleted'] == 0:
                return jsonify({'code':400, 'message':'The id is invalid. This can happen if the item represented by the id has been deleted.'})
            else:    
                return jsonify({'code':200, 'message':'Success!'})
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})
    
    def update_building_by_id(self, building_id: str, env_id: str, 
                              name: str, num_floors: int, description: str,
                              latitude: float, longitude: float, altitude: float,
                              is_public: bool, is_active: bool) -> dict:
        try:
            self.verify_db()
            self.verify_table()
            building = r.db(self.database_name).table(self.table_name).get(building_id).update({
                              'env_id': env_id, 
                              'name': name, 
                              'num_floors': num_floors, 
                              'description': description,
                              'latitude': latitude, 
                              'longitude': longitude, 
                              'altitude': altitude,
                              'is_public': is_public, 
                              'is_active': is_active
                              }).run(g.rdb_conn)
            if building['replaced'] == 0:
                return jsonify({'code':400, 'message':'The id is invalid. This can happen if the item represented by the id has been deleted.'})
            else:    
                return jsonify({'code':200, 'message':'Success!'})
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})