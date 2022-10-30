import json
import os
from pydoc import cli
from dotenv import load_dotenv
from application.core.exceptions.status_codes import CreatedResponseCode, DeletedResponseCode
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from application.data.datasource.ble_datasource import IBleDatasource
from flask import jsonify, abort, g
from application.core.exceptions.status_codes import (SuccessResponseCode, DeletedResponseCode, InternalServerErrorResponseCode, NotFoundResponseCode)
 
r = RethinkDB()

class BleDatasourceImpl(IBleDatasource):
    def __init__(self, database_name: str, table_name: str) -> None:
        self.database_name = database_name
        self.table_name = table_name
    
    def get_ble_by_id(self, ble_id: str) -> dict:
        """
        Get BLE fingerprints by BLE ID
        Parameters:
        ble_id: BLE fingerprint ID
        Return:
        BLE data (dict)
        """
        try:
            # Get BLE data from the database using the ID
            ble = r.db(self.database_name).table(self.table_name).get(ble_id).to_json().run(g.rdb_conn)
    
            if ble is None or ble=='null':
                return NotFoundResponseCode(message="BLE ID not found.")
            
            return json.loads(ble)
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message)
    
    def get_ble_by_fingerprint_id(self, fingerprint_id: str) -> dict:
        """
        Get BLE fingerprints by Fingerprint ID
        Parameters:
        fingerprint_id: Fingerprint ID
        Return: 
        Ble data (dict)
        """
        try:
            # Get BLE data from the database using the fingerprint ID
            bles = r.db(self.database_name).table(self.table_name).filter({"fingerprint_id": fingerprint_id}).run(g.rdb_conn)
            if bles==None or bles=="null":
                return NotFoundResponseCode(message="Fingerprint ID not found.")
            
            list_bles = []
            for ble in bles:
                list_bles.append(ble)
                
            if not list_bles:
                return jsonify({})
            
            return jsonify(list_bles)
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message) 
        
    def insert_ble(self, data: json) -> dict:
        
        try:
            insert = r.db(self.database_name).table(self.table_name).insert(data).run(g.rdb_conn)
            return CreatedResponseCode()
            
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message) 
    
    def delete_ble_by_id(self, ble_id: str) -> dict:
        try:
            ble = r.db(self.database_name).table(self.table_name).get(ble_id).delete().run(g.rdb_conn)
            if ble['deleted'] == 0:
                return NotFoundResponseCode(message="BLE ID not found.")
            else:    
                return SuccessResponseCode()
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message) 
    
    def delete_ble_by_fingerprint_id(self, fingerprint_id: str) -> dict:
        try:
            fingerprit = r.db(self.database_name).table(self.table_name).filter({'fingerprint_id': fingerprint_id}).delete().run(g.rdb_conn)

            if fingerprit['deleted'] == 0:
                return NotFoundResponseCode(message="Fingerprint ID not found.")
            else:    
                return SuccessResponseCode()
        except RqlRuntimeError as e:
            return InternalServerErrorResponseCode(message=e.message) 