from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
from appwrite.exception import AppwriteException
from appwrite.query import Query
from application.data.datasource.model_datasource import IModelDatasource
from application.core.exceptions.status_codes import (ErrorCode, SuccessCode)
from flask import jsonify
from datetime import datetime
import time
import json
import os

class ModelDatasourceImpl(IModelDatasource):
    def __init__(self, client: Client, database_name: str, tables: dict) -> None:
        self.database_name = database_name
        self.tables = tables
        self.client = client
        
    def train_model(self, data: json, model: str) -> dict:
        try:
            millisecond = datetime.now()
            created= time.mktime(millisecond.timetuple()) * 1000
            
            data['created_at'] = str(created)
            
            data = json.dumps(data)
            
            process_file = os.path.join(os.getcwd(),'application', 'algorithm')
            
            os.system('python ' + process_file + '/process_cnn_elm.py'
                                ' --params ' + "'" + str(data) + "' &")
            
            return SuccessCode()
        except AppwriteException as e:
            return ErrorCode(message=e.message)
    
    def get_model_by_id(self, model_id: str) -> dict:
        return super().get_model_by_id(model_id)
    
    def get_model_by_name(self, name: str) -> dict:
        return super().get_model_by_name(name)
    
    def delete_model_by_id(self, model_id: str) -> dict:
        return super().delete_model_dataset(model_id)