import json
import os
from subprocess import PIPE, Popen, STDOUT

from appwrite.client import Client
from appwrite.services.users import Users
from appwrite.exception import AppwriteException
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
from appwrite.query import Query

from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from application.data.datasource.preprocessing_datasource import IPreprocessingDatasource
from flask import jsonify, g
from datetime import datetime
import time

r = RethinkDB()

class PreprocessingDatasourceImpl(IPreprocessingDatasource):
    def __init__(self, client: Client, database_name: str, table_config: str, table_data: str, table_dataset: str) -> None:
        self.database_name = database_name
        self.table_data = table_data
        self.table_config = table_config
        self.table_dataset = table_dataset
        self.client = client
        
    
    def verify_rethinkdb(self) -> dict:
        try:
            list_databases = r.db_list().run(g.rdb_conn)
            
            if not self.database_name in list_databases:
                r.db_create(self.database_name).run(g.rdb_conn)
                r.db(self.database_name).table_create(self.table_name).run(g.rdb_conn)
                pass
        except RqlRuntimeError as e:
            return jsonify({'code': '0', 'message': e.message})
        
    def get_data_preprocessed_by_id(self, conf_prepro_id: str) -> dict:
        try:
            databases = Databases(self.client)
            documents = databases.list_documents(self.database_name, self.table_config,
                                              queries=[Query.equal('id_preprocessing', conf_prepro_id)])
            data = {}
            if documents['total'] != 0:
                for document in documents['documents']:
                    data[document['parameter']] = document['value']
                
                return jsonify(data)
                
            return jsonify({'code':404, 'message': 'File not found.'})
        except AppwriteException as e:
            return jsonify({'code':501, 'message': e.message})
    
    def preprocess_data(self, data: json) -> dict:
        try:
            self.verify_rethinkdb()
            
            millisecond = datetime.now()
            created= time.mktime(millisecond.timetuple()) * 1000
            
            insert_data = json.dumps({
                'name': data['name'],
                'env_id': data['env_id'],
                'building_id': data['building_id'],
                'floor_id': data['floor_id'],
                'data_representation': data['data_representation'],
                'x_normalization' : data['x_normalization'],
                'y_normalization' : data['y_normalization'],
                'pos_tech_id': data['pos_tech_id'],
                'date_start': data['date_start'],
                'date_end': data['date_end'],
                'non_dected_value': data['non_dected_value'],
                'is_active': data['is_active'],
                'created_at': created,
                'updated_at': created
            })
            
            databases = Databases(self.client)
            documents = databases.list_documents(self.database_name, self.table_dataset,
                                              queries=[Query.equal('name', data['name'])])

            if documents['total'] == 0:
                process_file = os.path.join(os.getcwd(),'application', 'data_preprocessing')
                
                os.system('python ' + process_file + '/preprocessing.py'
                        ' --params ' + "'" + str(insert_data) + "' &")
            
                return jsonify({'code':200, 'message': 'Processing...'})
            
            return jsonify({'code':409, 'message': 'This register already exists.'})
            
        except AppwriteException as e:
            return jsonify({'code':501, 'message':e.message})
    
    
    def delete_data_preprocessed_by_id(self, conf_prepro_id: str) -> dict:
        try:
            storage = Storage(self.client)
            databases = Databases(self.client)
            documents = databases.list_documents(self.database_name, self.table_config,
                                              queries=[Query.equal('id_preprocessing', conf_prepro_id)])
            
            # Get IDs of preprocessing and file tables
            list_ids_config = []
            list_files_config = []
            if documents['total'] != 0:
                for document in documents['documents']:
                    list_ids_config.append(document['$id'])
                    parameter = document['parameter'].split('_')
                    last_word_parameter = parameter[-1]
                    if last_word_parameter == 'file':
                        list_files_config.append(document['value'])
            
                # Get ID datasets
                datasets = databases.list_documents(self.database_name, self.table_dataset,
                                                    queries=[Query.equal('process_id', conf_prepro_id)])
                list_datasets = []
                
                for dataset in datasets['documents']:
                    list_datasets.append(dataset['$id'])
                
                # Remove records from preprocessing table
                for id in list_ids_config:
                    result = databases.delete_document(self.database_name, self.table_config, id)
                    
                # Remove records from Dataset table
                for dataset_id in list_datasets:
                    result = databases.delete_document(self.database_name, self.table_dataset, dataset_id)
                
                # Remove records from Dataset table
                for file in list_files_config:
                    result = storage.delete_file(self.table_data, file)
                    
                return jsonify({'code':200, 'message': 'Sucess!'})
            
            return jsonify({'code':204, 'message': 'No content.'})
            
        except AppwriteException as e:
            return jsonify({'code':501, 'message':e.message})
        
    def get_data_preprocessed_by_env(self, env_id: str) -> dict:
        try:
            databases = Databases(self.client)
            documents = databases.list_documents(self.database_name, self.table_config,
                                              queries=[Query.equal('value', env_id)])
            if documents['documents']!=0:
                list_ids = []
                for document in documents['documents']:
                    list_ids.append(document['id_preprocessing'])
                
                list_documents = []
                for id in list_ids:
                    documents = databases.list_documents(self.database_name, self.table_config,
                                                queries=[Query.equal('id_preprocessing', id)])
                    data = {}
                    if documents['total'] != 0:
                        data['id_preprocessing'] = id
                        for document in documents['documents']:
                            data[document['parameter']] = document['value']
                    
                    list_documents.append(data)
            
                return jsonify(list_documents)
            return jsonify({'code':204, 'message':'No content.'})
        except AppwriteException as e:
            return jsonify({'code':501, 'message':e.message})