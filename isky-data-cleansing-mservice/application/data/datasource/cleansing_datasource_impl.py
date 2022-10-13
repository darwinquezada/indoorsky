from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
from appwrite.exception import AppwriteException
from appwrite.query import Query
from application.data.datasource.cleansing_datasource import IDataCleansingDatasource
from flask import jsonify
from datetime import datetime
import time
import json
import os


class DataCleansingDatasourceImpl(IDataCleansingDatasource):
    def __init__(self, client: Client, database_name: str, tables: dict) -> None:
        self.database_name = database_name
        self.tables = tables
        self.client = client
        
    def clean_dataset(self, data: json) -> dict:
        try:
            millisecond = datetime.now()
            created= time.mktime(millisecond.timetuple()) * 1000
            data_completed = json.dumps({
                'name': data['name'],
                'threshold': data['threshold'],
                'dataset_id': data['dataset_id'],
                'test': {
                    'percent_test': data['test']['percent_test'],
                    'test_accuracy': data['test']['test_accuracy'],
                    'k': data['test']['k'],
                    'distance_metric': data['test']['distance_metric']
                },
                'created_at': created
            })
            
            databases = Databases(self.client)
            documents = databases.list_documents(self.database_name, self.tables['cleansing'],
                                              queries=[Query.equal('value', data['name'])])
            
            documents_datasets = databases.list_documents(self.database_name, self.tables['dataset'],
                                              queries=[Query.equal('$id', data['dataset_id'])])
            

            if documents['total'] == 0:
                if documents_datasets['total'] != 0:
                    process_file = os.path.join(os.getcwd(),'application', 'algorithm')
                    os.system('python ' + process_file + '/process.py'
                                ' --params ' + "'" + str(data_completed) + "' &")
                    return jsonify({'code':200, 'message':'Processing...'})
                else:
                    return jsonify({'code':204, 'message':'Dataset ID is not valid.'})
            
            return jsonify({'code':409, 'message': 'This register already exists.'})
        except AppwriteException as e:
                return jsonify({'code':501, 'message':e.message})
        
    def get_cleansed_dataset_by_id(self, clean_id: str) -> dict:
        try:
            databases = Databases(self.client)
            documents = databases.list_documents(self.database_name, self.tables['cleansing'],
                                              queries=[Query.equal('id_cleansing', clean_id)])

            list_parameters = {}
            results = {}
            test = {}
            if documents['total'] != 0:
                list_cleansed_params = databases.list_documents(self.database_name, self.tables['cleansing'],
                                                                queries=[Query.equal('id_cleansing', clean_id)])
                for data in list_cleansed_params['documents']:
                    parameter = data['parameter'].split('.')
                    if len(parameter) > 1:
                        if parameter[0] == 'result':
                            results[parameter[1]] = data['value']
                        else:
                            test[parameter[1]] = data['value']
                    else:
                        list_parameters[data['parameter']] = data['value']
                
                list_parameters['cleansing_id'] = clean_id
                list_parameters['results'] = results
                list_parameters['test'] = test
                
                return jsonify(list_parameters)
            else:
                return jsonify({'code':404, 'message':'Data cleansed ID does not exist.'})
        except AppwriteException as e:
            return jsonify({'code':501, 'message':e.message})
    
    def get_cleansed_dataset_by_env(self, env_id: str) -> dict:
        return super().get_cleansed_dataset_by_env(env_id)
    
    def delete_cleansed_dataset(self, clean_id: str) -> dict:
        try:
            storage = Storage(self.client)
            databases = Databases(self.client)
            documents = databases.list_documents(self.database_name, self.tables['cleansing'],
                                              queries=[Query.equal('id_cleansing', clean_id)])
            
            if documents['total'] != 0:
                for document in documents['documents']:
                    databases.delete_document(self.database_name, self.tables['cleansing'], document['$id'])
                
                documents_preprocessing = databases.list_documents(self.database_name, self.tables['preprocessing'],
                                              queries=[Query.equal('id_preprocessing', clean_id)])
                
                for preprocess in documents_preprocessing['documents']:
                    databases.delete_document(self.database_name, self.tables['preprocessing'], preprocess['$id'])
                    storage.delete_file(self.tables['file_preprocessing'], preprocess['value'])
                    
                
                documents_datasets = databases.list_documents(self.database_name, self.tables['dataset'],
                                              queries=[Query.equal('process_id', clean_id)])
                
                for dataset in documents_datasets['documents']:
                    databases.delete_document(self.database_name,  self.tables['dataset'], dataset['$id'])
                
                return jsonify({'code':200, 'message':'Success!'})
            
            return jsonify({'code':404, 'message':'Data cleansed ID does not exist.'})
        except AppwriteException as e:
            return jsonify({'code':501, 'message':e.message})
    
    def get_cleansed_dataset_by_name(self, name: str) -> dict:
        try:
            databases = Databases(self.client)
            documents = databases.list_documents(self.database_name, self.tables['cleansing'],
                                              queries=[Query.equal('value', name)])

            list_parameters = {}
            results = {}
            test = {}
            if documents['total'] != 0:
                list_cleansed_params = databases.list_documents(self.database_name, self.tables['cleansing'],
                                                                queries=[Query.equal('id_cleansing', 
                                                                                     documents['documents'][0]['id_cleansing'])])
                for data in list_cleansed_params['documents']:
                    parameter = data['parameter'].split('.')
                    if len(parameter) > 1:
                        if parameter[0] == 'result':
                            results[parameter[1]] = data['value']
                        else:
                            test[parameter[1]] = data['value']
                    else:
                        list_parameters[data['parameter']] = data['value']
                
                list_parameters['cleansing_id'] = documents['documents'][0]['id_cleansing']
                list_parameters['results'] = results
                list_parameters['test'] = test
                
                return jsonify(list_parameters)
            else:
                return jsonify({'code':404, 'message':'Data cleansed name does not exist.'})
        except AppwriteException as e:
            return jsonify({'code':501, 'message':e.message})