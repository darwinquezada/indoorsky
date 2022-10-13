import json
import os
from pydoc import cli
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from application.data.datasource.pos_tech_datasource import IPosTechDatasource
from flask import jsonify, abort, g
from application.core.exceptions.status_codes import CreateSuccessCode, DeleteSuccessCode

r = RethinkDB()

class PosTechDatasourceImpl(IPosTechDatasource):
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
                r.db(self.database_name).table(self.table_name).index_create("code").run(g.rdb_conn)
                r.db(self.database_name).table(self.table_name).index_wait("name").run(g.rdb_conn)
                r.db(self.database_name).table(self.table_name).index_wait("code").run(g.rdb_conn)

                pass
        except RqlRuntimeError as e:
            return jsonify({'code': '0', 'message': e.message})
        
    def insert_pos_tech(self, data: json) -> dict:
        try:
            self.verify_db()
            self.verify_table()
            
            filter_predicate = {
                "name": data['name'],
                "code": data['name']
            }
            
            reg_exist = r.db(self.database_name).table(self.table_name).filter(filter_predicate).count().eq(0).run(g.rdb_conn)
            
            if reg_exist == True:
                insert = r.db(self.database_name).table(self.table_name).insert(data).run(g.rdb_conn)
                return jsonify({'code':200, 'message':'Success!'})
            else:
                return jsonify({'code':409, 'message':'Oops ... you\'re trying to create an already existing record.'})
            
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})
    
    def get_pos_tech_by_id(self, pos_tech_id: str) -> dict:
        try:
            pos_tech = r.db(self.database_name).table(self.table_name).get(pos_tech_id).to_json().run(g.rdb_conn)
            if pos_tech==None:
                return jsonify({'code':204, 'message':'Oops ... No content'})
            
            return json.loads(pos_tech)
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e})
    
    def get_pos_tech_by_name(self, name: str) -> dict:
        try:
            pos_technologies = r.db(self.database_name).table(self.table_name).filter({"name": name}).run(g.rdb_conn)

            if pos_technologies==None:
                return jsonify({'code':204, 'message':'Oops ... No content'})
            
            list_pos_technologies = []
            for pos_technology in pos_technologies:
                list_pos_technologies.append(pos_technology)
                
            if not list_pos_technologies:
                return jsonify({'code':204, 'message':'Oops ... No content'})
            
            return jsonify(list_pos_technologies)
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})
    
    def update_pos_tech_by_id(self, pos_tech_id: str, data: json) -> dict:
        try:
            pos_tech = r.db(self.database_name).table(self.table_name).get(pos_tech_id).update(data).run(g.rdb_conn)
            if pos_tech['replaced'] == 0:
                return jsonify({'code':400, 'message':'The id is invalid. This can happen if the item represented by the id has been deleted.'})
            else:    
                return jsonify({'code':200, 'message':'Success!'})
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})
    
    def delete_pos_tech_by_id(self, pos_tech_id: str) -> dict:
        try:
            pos_tech = r.db(self.database_name).table(self.table_name).get(pos_tech_id).delete().run(g.rdb_conn)
            if pos_tech['deleted'] == 0:
                return jsonify({'code':400, 'message':'The id is invalid. This can happen if the item represented by the id has been deleted.'})
            else:    
                return jsonify({'code':200, 'message':'Success!'})
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})