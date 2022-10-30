import json
import os
from pydoc import cli
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from application.data.datasource.floor_datasource import IFloorDatasource
from flask import jsonify, abort, g
from application.core.exceptions.status_codes import (SuccessResponseCode, 
                                                      InternalServerErrorResponseCode, 
                                                      NotFoundResponseCode, 
                                                      ConflictResponseCode)

r = RethinkDB()

class FloorDatasourceImpl(IFloorDatasource):
    def __init__(self, database_name: str, table_name: str) -> None:
        self.database_name = database_name
        self.table_name = table_name
        
    def insert_floor(self, data: json) -> dict:
        try:
            
            filter_predicate = {
                "building_id": data['building_id'],
                "level": data['level']
            }
            
            reg_exist = r.db(self.database_name).table(self.table_name).filter(filter_predicate).count().eq(0).run(g.rdb_conn)
            
            if reg_exist == True:
                insert = r.db(self.database_name).table(self.table_name).insert(data).run(g.rdb_conn)
                return SuccessResponseCode()
            else:
                return ConflictResponseCode(message="There is a record with the same parameters.")
            
        except RqlRuntimeError as e:
            InternalServerErrorResponseCode(message=e.message)
    
    def get_floor_by_id(self, floor_id: str) -> dict:
        try:
            floor = r.db(self.database_name).table(self.table_name).get(floor_id).to_json().run(g.rdb_conn)
            
            if floor==None or floor=="null":
                return NotFoundResponseCode(message="Floor ID not found.")
            
            return json.loads(floor)
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)
    
    def get_floor_by_level(self, level: str) -> dict:
        try:
            floors = r.db(self.database_name).table(self.table_name).filter({"level": level}).run(g.rdb_conn)

            if floors==None or floors=="null":
                return NotFoundResponseCode(message="Level not found.")
            
            list_floors = []
            for floor in floors:
                list_floors.append(floor)
                
            if not list_floors:
                return NotFoundResponseCode()
            
            return jsonify(list_floors)
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)
    
    def delete_floor(self, floor_id: str) -> dict:
        try:
            floor = r.db(self.database_name).table(self.table_name).get(floor_id).delete().run(g.rdb_conn)
            if floor['deleted'] == 0:
                return NotFoundResponseCode(message="Floor ID not found.")
            else:    
                return SuccessResponseCode()
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)
    
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
                return NotFoundResponseCode(message="Floor ID not found")
            else:    
                return SuccessResponseCode()
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)