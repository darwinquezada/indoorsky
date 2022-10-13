import json
import os
from pydoc import cli
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from application.data.datasource.poi_datasource import IPoiDatasource
from flask import jsonify, abort, g
from application.core.exceptions.status_codes import CreateSuccessCode, DeleteSuccessCode
from datetime import datetime

r = RethinkDB()

class PoiDatasourceImpl(IPoiDatasource):
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
                r.db(self.database_name).table(self.table_name).index_create("floor_id").run(g.rdb_conn)
                r.db(self.database_name).table(self.table_name).index_wait("name").run(g.rdb_conn)
                r.db(self.database_name).table(self.table_name).index_wait("floor_id").run(g.rdb_conn)
                pass

        except RqlRuntimeError as e:
            return jsonify({'code': '0', 'message': e.message})

    def insert_poi(self, data: json) -> dict:
        try:
            self.verify_db()
            self.verify_table()

            millisecond = datetime.now()
            created = time.mktime(millisecond.timetuple()) * 1000

            filter_predicate = {
                "name": data['name'],
                "floor_id": data['floor_id'],
                "latitude": data['latitude'],
                "longitude": data['longitude'],
                "altitude": data['altitude'],
                "pos_x": data['pos_x'],
                "pos_y": data['pos_y'],
                "pos_z": data['pos_z'],
                "created_at": created,
                "updated_at": created
            }

            reg_exist = r.db(self.database_name).table(self.table_name).filter(filter_predicate).count().eq(0).run(g.rdb_conn)

            if reg_exist == True:
                insert = r.db(self.database_name).table(self.table_name).insert(data).run(g.rdb_conn)

                return jsonify({'code':200, 'message':'Success!'})
            else:
                return jsonify({'code':409, 'message':'Oops ... you\'re trying to create an already existing record.'})

        except RuntimeError as e:
            return jsonify({'code':501, 'message':e.args})

    def get_poi_by_id(self, poi_id: str) -> dict:
        try:
            poi = r.db(self.database_name).table(self.table_name).get(poi_id).to_json().run(g.rdb_conn)

            if poi==None:
                return jsonify({'code':204, 'message':'Oops ... No content'})

            return json.loads(poi)
        except RuntimeError as e:
            return jsonify({'code':501, 'message':e})

    def get_poi_by_name(self, name: str) -> dict:
        try:
            pois = r.db(self.database_name).table(self.table_name).filter({"name": name}).run(g.rdb_conn)

            if pois==None:
                return jsonify({'code':204, 'message':'Oops ... No content'})

            list_pois = []
            for poi in pois:
                list_pois.append(poi)

            if not list_pois:
                return jsonify({'code':204, 'message':'Oops ... No content'})

            return jsonify(list_pois)
        except RuntimeError as e:
            return jsonify({'code':501, 'message':e.args})

    def delete_poi(self, poi_id: str) -> dict:
        try:
            poi = r.db(self.database_name).table(self.table_name).get(poi_id).delete().run(g.rdb_conn)

            if poi['deleted'] == 0:
                return jsonify({'code':400, 'message':'The id is invalid. This can happen if the item represented by the id has been deleted.'})
            else:
                return jsonify({'code':200, 'message':'Success!'})
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})

    def update_poi_by_id(self, poi_id: str, floor_id: str, name: str, description: str, image: str,
                         latitude: float, longitude: float, altitude: float, pos_x: float,
                         pos_y: float, pos_z: float, is_active: bool, is_public: bool) -> dict:
        try:
            poi = r.db(self.database_name).table(self.table_name).get(poi_id).update({
                                                                    "floor_id": floor_id,
                                                                    "name": name,
                                                                    "description": description,
                                                                    "image": image,
                                                                    "latitude": latitude,
                                                                    "longitude": longitude,
                                                                    "altitude": altitude,
                                                                    "pos_x": pos_x,
                                                                    "pos_y": pos_y,
                                                                    "pos_z": pos_z,
                                                                    "is_active": is_active,
                                                                    "is_public": is_public
                                                                }).run(g.rdb_conn)

            if poi['replaced'] == 0:
                return jsonify({'code':400, 'message':'The id is invalid. This can happen if the item represented by the id has been deleted.'})
            else:
                return jsonify({'code':200, 'message':'Success!'})
        except RqlRuntimeError as e:
            return jsonify({'code':501, 'message':e.args})
