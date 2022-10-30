from ast import Not
import json
import os
from pydoc import cli
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from application.data.datasource.poi_datasource import IPoiDatasource
from flask import jsonify, abort, g
from application.core.exceptions.status_codes import (SuccessResponseCode, 
                                                      NotFoundResponseCode, 
                                                      InternalServerErrorResponseCode, 
                                                      ConflictResponseCode)
from datetime import datetime
import time

r = RethinkDB()

class PoiDatasourceImpl(IPoiDatasource):
    def __init__(self, database_name: str, table_name: str) -> None:
        self.database_name = database_name
        self.table_name = table_name

    def insert_poi(self, data: json) -> dict:
        try:
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

                return SuccessResponseCode()
            else:
                return ConflictResponseCode(message="There is a record with the same parameters.")

        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)

    def get_poi_by_id(self, poi_id: str) -> dict:
        try:
            poi = r.db(self.database_name).table(self.table_name).get(poi_id).to_json().run(g.rdb_conn)

            if poi==None or poi=="null":
                return NotFoundResponseCode(message="POI ID not found.")

            return json.loads(poi)
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)

    def get_poi_by_name(self, name: str) -> dict:
        try:
            pois = r.db(self.database_name).table(self.table_name).filter({"name": name}).run(g.rdb_conn)

            if pois==None or pois=="null":
                return NotFoundResponseCode(message="Name not found.")

            list_pois = []
            for poi in pois:
                list_pois.append(poi)

            if not list_pois:
                return NotFoundResponseCode()

            return jsonify(list_pois)
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)

    def delete_poi(self, poi_id: str) -> dict:
        try:
            poi = r.db(self.database_name).table(self.table_name).get(poi_id).delete().run(g.rdb_conn)

            if poi['deleted'] == 0:
                return NotFoundResponseCode(message="POI ID not found.")
            else:
                return SuccessResponseCode()
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)

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
                return NotFoundResponseCode(message="POI ID not found.")
            else:
                return SuccessResponseCode()
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)
