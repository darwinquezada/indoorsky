from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
from appwrite.exception import AppwriteException
from appwrite.query import Query
from application.data.datasource.model_datasource import IModelDatasource
from application.core.exceptions.status_codes import (SuccessResponseCode, ConflictResponseCode, 
                                                      NotFoundResponseCode, InternalServerErrorResponseCode)
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
            
            # Verify if the dataset exists
            process_file = os.path.join(os.getcwd(),'application', 'algorithm')
            
            databases = Databases(self.client)
            
            models = databases.list_documents(self.database_name, self.tables['model'],
                                              queries=[Query.equal('value', data['name'])])
            
            documents_datasets = databases.list_documents(self.database_name, self.tables['dataset'],
                                              queries=[Query.equal('$id', data['dataset_id'])])
            
            data['created_at'] = str(created)
            data = json.dumps(data)
            
            if models['total'] == 0:
                if documents_datasets['total'] != 0:
                    if model == 'cnn_elm':
                        os.system('python ' + process_file + '/process_cnn_elm.py'
                                            ' --params ' + "'" + str(data) + "' &")
                    else:
                        os.system('python ' + process_file + '/process_cnn_lstm.py'
                                            ' --params ' + "'" + str(data) + "' &")
                else:
                    return NotFoundResponseCode()        
            else:
                return ConflictResponseCode(message="There is a register with the same name.")   
                
            return SuccessResponseCode(message="Processing")
        except AppwriteException as e:
            return InternalServerErrorResponseCode(message=e.message)
    
    def get_model_by_id(self, model_id: str) -> dict:
        try:
            databases = Databases(self.client)
            documents = databases.list_documents(self.database_name, self.tables['model'],
                                              queries=[Query.equal('id_model', model_id)])

            list_parameters = {}
            results = {}
            floor = {}
            building = {}
            positioning = {}
            test = {}

            if documents['total'] != 0:
                list_model_params = databases.list_documents(self.database_name, self.tables['model'],
                                                                queries=[Query.equal('id_model',
                                                                                     documents['documents'][0]['id_model'])])
                for data in list_model_params['documents']:
                    parameter = data['parameter'].split('.')
                    if len(parameter) > 1:
                        if parameter[0] == 'result':
                            results[parameter[1]] = data['value']
                        elif parameter[0] == 'floor':
                            floor[parameter[1]] = data['value']
                        elif parameter[0] == 'building':
                            building[parameter[1]] = data['value']
                        elif parameter[0] == 'position':
                            positioning[parameter[1]] = data['value']
                        else:
                            test[parameter[1]] = data['value']
                    else:
                        list_parameters[data['parameter']] = data['value']

                list_parameters['model_id'] = documents['documents'][0]['id_model']
                list_parameters['floor'] = floor
                list_parameters['building'] = building
                list_parameters['position'] = positioning
                list_parameters['test'] = test
                list_parameters['results'] = results

                return jsonify(list_parameters)
            else:
                return NotFoundResponseCode(message="Model ID not found.")
        except AppwriteException as e:
            return InternalServerErrorResponseCode(message=e.message)
    
    def get_model_by_name(self, name: str) -> dict:
        try:
            databases = Databases(self.client)
            documents = databases.list_documents(self.database_name, self.tables['model'],
                                              queries=[Query.equal('value', name)])

            list_parameters = {}
            results = {}
            floor = {}
            building = {}
            positioning = {}
            test = {}
            
            if documents['total'] != 0:
                list_model_params = databases.list_documents(self.database_name, self.tables['model'],
                                                                queries=[Query.equal('id_model', 
                                                                                     documents['documents'][0]['id_model'])])
                
                
                for data in list_model_params['documents']:
                    parameter = data['parameter'].split('.')
                    if len(parameter) > 1:
                        if parameter[0] == 'result':
                            results[parameter[1]] = data['value']
                        elif parameter[0] == 'floor':
                            floor[parameter[1]] = data['value']
                        elif parameter[0] == 'building':
                            building[parameter[1]] = data['value']
                        elif parameter[0] == 'position':
                            positioning[parameter[1]] = data['value']
                        else:
                            test[parameter[1]] = data['value']
                    else:
                        list_parameters[data['parameter']] = data['value']
                
                list_parameters['model_id'] = documents['documents'][0]['id_model']
                list_parameters['floor'] = floor
                list_parameters['building'] = building
                list_parameters['position'] = positioning
                list_parameters['test'] = test
                list_parameters['results'] = results
                
                return jsonify(list_parameters)
            else:
                return NotFoundResponseCode(message="Model name not found.")
        except AppwriteException as e:
            return InternalServerErrorResponseCode(message=e.message)
    
    def delete_model_by_id(self, model_id: str) -> dict:
        try:
            storage = Storage(self.client)
            databases = Databases(self.client)
            documents = databases.list_documents(self.database_name, self.tables['model'],
                                              queries=[Query.equal('id_model', model_id)])
            
            if documents['total'] != 0:
                for document in documents['documents']:
                    # Remove documents
                    databases.delete_document(self.database_name, self.tables['model'], document['$id'])
                    # Remove files from the datastore
                    if document['parameter'] == 'building_model' or document['parameter'] == 'floor_model' or document['parameter'] == 'positioning_model':
                        storage.delete_file(self.tables['file_model'], document['value'])
                
                return SuccessResponseCode()
            
            return NotFoundResponseCode(message="Data cleansing ID not found.")
        except AppwriteException as e:
            return InternalServerErrorResponseCode(message=e.message)