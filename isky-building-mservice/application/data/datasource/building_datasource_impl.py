import json
import os
from pydoc import cli
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from application.data.datasource.building_datasource import IBuildingDatasource
from flask import jsonify, abort, g
from application.core.exceptions.status_codes import (CreatedResponseCode, 
                                                      InternalServerErrorResponseCode, 
                                                      SuccessResponseCode, 
                                                      NotFoundResponseCode,
                                                      ConflictResponseCode)

r = RethinkDB()

class BuildingDatasourceImpl(IBuildingDatasource):
    def __init__(self, database_name: str, table_name: str) -> None:
        self.database_name = database_name
        self.table_name = table_name
        
    def insert_building(self, data: json) -> dict:
        try:
            
            filter_predicate = {
                "name": data['name'],
                "env_id": data['env_id']
            }
            
            reg_exist = r.db(self.database_name).table(self.table_name).filter(filter_predicate).count().eq(0).run(g.rdb_conn)
            
            if reg_exist == True:
                insert = r.db(self.database_name).table(self.table_name).insert(data).run(g.rdb_conn)
                return CreatedResponseCode()
            else:
                return ConflictResponseCode(message="A register with the name and environment ID already exists in the table.")
            
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)
    
    def get_building_by_id(self, building_id: str) -> dict:
        try:
            
            building = r.db(self.database_name).table(self.table_name).get(building_id).to_json().run(g.rdb_conn)
            if building=='null':
                return NotFoundResponseCode(message="Building ID not found.")
            
            return json.loads(building)
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)
    
    def get_building_by_name(self, name: str) -> dict:
        try:
            
            buildings = r.db(self.database_name).table(self.table_name).filter({"name": name}).run(g.rdb_conn)
            
            buildings = list(buildings)
            
            if buildings=='null' or not buildings:
                return NotFoundResponseCode(message="Name not found.")
            
            list_buildings = []
            for building in buildings:
                list_buildings.append(building)
                
            if not list_buildings:
                return NotFoundResponseCode()
            
            return jsonify(list_buildings)
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)
    
    def delete_building(self, building_id: str) -> dict:
        try:
            building = r.db(self.database_name).table(self.table_name).get(building_id).delete().run(g.rdb_conn)
            if building['deleted'] == 0:
                return NotFoundResponseCode(message="Building ID not found.")
            else:    
                return SuccessResponseCode()
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)
    
    def update_building_by_id(self, building_id: str, env_id: str, 
                              name: str, num_floors: int, description: str,
                              latitude: float, longitude: float, altitude: float,
                              is_public: bool, is_active: bool) -> dict:
        try:
            
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
                return NotFoundResponseCode(message="Building ID not found.")
            else:    
                return SuccessResponseCode()
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)