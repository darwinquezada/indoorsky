import json
import os
from pydoc import cli
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from application.data.datasource.pos_tech_datasource import IPosTechDatasource
from flask import jsonify, abort, g
from application.core.exceptions.status_codes import (SuccessResponseCode, 
                                                      ConflictResponseCode, 
                                                      InternalServerErrorResponseCode, 
                                                      NotFoundResponseCode)

r = RethinkDB()

class PosTechDatasourceImpl(IPosTechDatasource):
    def __init__(self, database_name: str, table_name: str) -> None:
        self.database_name = database_name
        self.table_name = table_name
        
    def insert_pos_tech(self, data: json) -> dict:
        try:
            filter_predicate = {
                "name": data['name'],
                "code": data['name']
            }
            
            reg_exist = r.db(self.database_name).table(self.table_name).filter(filter_predicate).count().eq(0).run(g.rdb_conn)
            
            if reg_exist == True:
                insert = r.db(self.database_name).table(self.table_name).insert(data).run(g.rdb_conn)
                return SuccessResponseCode()
            else:
                return ConflictResponseCode(message="There is a record with the same name and code.")
            
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)
    
    def get_pos_tech_by_id(self, pos_tech_id: str) -> dict:
        try:
            pos_tech = r.db(self.database_name).table(self.table_name).get(pos_tech_id).to_json().run(g.rdb_conn)
            if pos_tech==None or pos_tech=="null":
                return NotFoundResponseCode(message="Positioning technology ID not found.")
            
            return json.loads(pos_tech)
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)
    
    def get_pos_tech_by_name(self, name: str) -> dict:
        try:
            pos_technologies = r.db(self.database_name).table(self.table_name).filter({"name": name}).run(g.rdb_conn)

            if pos_technologies==None or pos_technologies=="null":
                return NotFoundResponseCode(message="Name not found.")
            
            list_pos_technologies = []
            for pos_technology in pos_technologies:
                list_pos_technologies.append(pos_technology)
                
            if not list_pos_technologies:
                return NotFoundResponseCode()
            
            return jsonify(list_pos_technologies)
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)
    
    def update_pos_tech_by_id(self, pos_tech_id: str, data: json) -> dict:
        try:
            pos_tech = r.db(self.database_name).table(self.table_name).get(pos_tech_id).update(data).run(g.rdb_conn)
            if pos_tech['replaced'] == 0:
                return NotFoundResponseCode(message="Positioning technology ID not found.")
            else:    
                return SuccessResponseCode()
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)
    
    def delete_pos_tech_by_id(self, pos_tech_id: str) -> dict:
        try:
            pos_tech = r.db(self.database_name).table(self.table_name).get(pos_tech_id).delete().run(g.rdb_conn)
            if pos_tech['deleted'] == 0:
                return NotFoundResponseCode(message="Positioning technology ID not found.")
            else:    
                return SuccessResponseCode()
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)