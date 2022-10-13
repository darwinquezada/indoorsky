import json
import os
from pydoc import cli
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from application.data.datasource.floor_datasource import IFloorDatasource
from flask import jsonify, abort, g
from application.core.exceptions.status_codes import CreateSuccessCode, DeleteSuccessCode

r = RethinkDB()

class FloorDatasourceImpl(IFloorDatasource):
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
                r.db(self.database_name).table(self.table_name).index_create("building_id").run(g.rdb_conn)
                r.db(self.database_name).table(self.table_name).index_create("level").run(g.rdb_conn)
                r.db(self.database_name).table(self.table_name).index_wait("building_id").run(g.rdb_conn)
                r.db(self.database_name).table(self.table_name).index_wait("level").run(g.rdb_conn)

                pass
        except RqlRuntimeError as e:
            return jsonify({'code': '0', 'message': e.message})
        
    def insert_floor(self, data: json) -> dict:
        try:
            self.verify_db()
            self.verify_table()
            
            filter_predicate = {
                "building_id": data['building_id'],
                "level": data['level']
            }
            
            reg_exist = r.db(self.database_name).table(self.table_name).filter(filter_predicate).count().eq(0).run(g.rdb_conn)
            
            if reg_exist == True:
                insert = r.db(self.database_name).table(self.table_name).insert(data).run(g.rdb_conn)
                return jsonify({'code':200, 'message':'Success!'})
            else:
                return jsonify({'code':409, 'message':'Oops ... you\'re trying to create an already existing record.'})
            
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})
    
    def get_floor_by_id(self, floor_id: str) -> dict:
        try:
            floor = r.db(self.database_name).table(self.table_name).get(floor_id).to_json().run(g.rdb_conn)
            if floor==None:
                return jsonify({'code':204, 'message':'Oops ... No content'})
            
            return json.loads(floor)
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e})
    
    def get_floor_by_level(self, level: str) -> dict:
        try:
            floors = r.db(self.database_name).table(self.table_name).filter({"level": level}).run(g.rdb_conn)

            if floors==None:
                return jsonify({'code':204, 'message':'Oops ... No content'})
            
            list_floors = []
            for floor in floors:
                list_floors.append(floor)
                
            if not list_floors:
                return jsonify({'code':204, 'message':'Oops ... No content'})
            
            return jsonify(list_floors)
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})
    
    def delete_floor(self, floor_id: str) -> dict:
        try:
            floor = r.db(self.database_name).table(self.table_name).get(floor_id).delete().run(g.rdb_conn)
            if floor['deleted'] == 0:
                return jsonify({'code':400, 'message':'The id is invalid. This can happen if the item represented by the id has been deleted.'})
            else:    
                return jsonify({'code':200, 'message':'Success!'})
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})
    
    def update_floor_by_id(self, floor_id: str, building_id: str,
                           level: str, is_public: bool, is_active: bool) -> dict:
        try:
            floor = r.db(self.database_name).table(self.table_name).get(floor_id).update({
                              'floor_id': floor_id, 
                              'building_id': building_id,
                              'level': level, 
                              'is_public': is_public, 
                              'is_active': is_active
                              }).run(g.rdb_conn)
            if floor['replaced'] == 0:
                return jsonify({'code':400, 'message':'The id is invalid. This can happen if the item represented by the id has been deleted.'})
            else:    
                return jsonify({'code':200, 'message':'Success!'})
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})