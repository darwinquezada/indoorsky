#!/usr/bin/python
from data_cleansing import clean_dataset
from data_partition import data_partition
from knn_positioning import Position_KNN

from appwrite.exception import AppwriteException
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.input_file import InputFile
from appwrite.query import Query
from appwrite.services.storage import Storage
from appwrite.input_file import InputFile

import numpy as np
from flask import jsonify
from dotenv import load_dotenv
from io import BytesIO
import re
import joblib
import argparse
import uuid
import json
import os

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)


client = Client()
client.set_endpoint(os.environ['APPWRITEENDPOINT'])
client.set_project(os.environ['APPWRITEPROJECTID'])
client.set_key(os.environ['APPWRITEAPIKEY'])

database_id = os.environ['RDB_DB']
config_preproc_id = os.environ['TABLE_PREPROCESSING']
bucket_preproc_id = os.environ['TABLE_FILE']
dataset_id = os.environ['TABLE_DATASET']
data_cleansing = os.environ['TABLE_CLEANSING']


def get_dataset(dataset: str):
    try:
        databases = Databases(client=client)
        documents = databases.get_document(database_id, dataset_id, dataset)
        data = json.dumps(documents)
        return str(data)
    except AppwriteException as e:
        print({'code': '0', 'message': e.message})


def get_data_preprocessed_by_id(conf_prepro_id: str):
        try:
            databases = Databases(client)
            documents = databases.list_documents(database_id, config_preproc_id,
                                              queries=[Query.equal('id_preprocessing', conf_prepro_id)])
            data = {}
            if documents['total'] != 0:
                for document in documents['documents']:
                    data[document['parameter']] = document['value']
                
                return json.dumps(data)
                
            return jsonify({'code':404, 'message': 'File not found.'})
        except AppwriteException as e:
            return jsonify({'code':501, 'message': e.message})


def upload_file(file_path:str) -> str:
    try:
        storage = Storage(client)
        response = storage.create_file(bucket_id=bucket_preproc_id, file_id='unique()', file=InputFile.from_path(file_path))
        return response['$id']
    except AppwriteException as e:
        print({'code': '0', 'message': e.message})


def insert_document(collection_id: str, data: dict) -> str:
    try:
        databases = Databases(client)
        response = databases.create_document(database_id=database_id, collection_id=collection_id, 
                                             document_id='unique()', data=data)
        return response['$id']
    except AppwriteException as e:
        print({'code': '0', 'message': e.message})
      
        
def insert_data(collection_id: str, id:str, parameter: str, value: str, path_file: str):
    
    if path_file != "":
        file_id = upload_file(path_file)
        value = file_id
           
    data = {
        "parameter": parameter,
        "value": value
        }
    if collection_id != data_cleansing:
        data["id_preprocessing"] = id
        data["type"] = "CLEANSING"
    else:
        data["id_cleansing"]=id
        
    insert_document(collection_id=collection_id, data=data)

def insert_dataset(name:str, technique: str, process_id: str):    
    data = {
        "name": name,
        "technique": technique,
        "type": "CLEANSING",
        "process_id": process_id
        }
    try:
        databases = Databases(client)
        response = databases.create_document(database_id=database_id, collection_id=dataset_id, 
                                             document_id='unique()', data=data)
        return response['$id']
    except AppwriteException as e:
        print({'code': '0', 'message': e.message})

if __name__ == '__main__':
    p = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description='')
    p.add_argument('--params', dest='params', action='store', default='', help='Arguments')
    
    args = p.parse_args()

    params = json.loads(args.params)
    
    # Create a temporal directory to store files
    temp_path = os.path.join(os.getcwd(), 'application', 'temp')
    
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    
    # Unique ID for all files generated during the preprocessing
    uuid_file = str(uuid.uuid1())
    
    # Save parameters
    insert_data(collection_id=data_cleansing, id=uuid_file, 
                parameter='name', value=params['name'], 
                path_file='')
    insert_data(collection_id=data_cleansing, id=uuid_file, 
                parameter='dataset_id', value=params['dataset_id'], 
                path_file='')
    insert_data(collection_id=data_cleansing, id=uuid_file, 
                parameter='threshod', value=str(params['threshold']), 
                path_file='')
    insert_data(collection_id=data_cleansing, id=uuid_file, 
                parameter='test.percent_test', value=str(params['test']['percent_test']), 
                path_file='')
    insert_data(collection_id=data_cleansing, id=uuid_file, 
                parameter='test.test_accuracy', value=str(params['test']['test_accuracy']), 
                path_file='')
    insert_data(collection_id=data_cleansing, id=uuid_file, 
                parameter='test.k', value=str(params['test']['k']), 
                path_file='')
    insert_data(collection_id=data_cleansing, id=uuid_file, 
                parameter='test.distance_metric', value=str(params['test']['distance_metric']), 
                path_file='')
    # Get dataset
    dataset_data = json.loads(get_dataset(dataset=params['dataset_id']))
    data_preprocessing = get_data_preprocessed_by_id(dataset_data['process_id'])
    
    data_preprocessing_to_json = json.loads(data_preprocessing)
    
    # Create a temporal directory to store files
    temp_path = os.path.join(os.getcwd(), 'application', 'temp')
    
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    
    storage = Storage(client)
    
    file = {}
    
    # Save files in the terporal dir 
    for key, value in data_preprocessing_to_json.items():
        parameter = key.split('_')
        if  parameter[-1] == 'file':
            load_file = storage.get_file_view(bucket_preproc_id, value)
            file_tranform = BytesIO(load_file)
            file[key] = joblib.load(file_tranform)
            
    if dataset_data['technique'] == 'NORMALIZATION':
        x_train_preprocessed = file['x_data_normalization_file']
    elif dataset_data['technique'] == 'TRANSFORMATION':
        x_train_preprocessed = file['x_data_transformed_file']
    else:
        x_train_preprocessed = file['x_data_original_file']
            
    y_train = file['y_data_original_file'].copy()
    # Rename columns
    y_train.columns = ['LONGITUDE','LATITUDE','ALTITUDE','FLOOR','BUILDINGID']
    
    y_train_temp = y_train.copy()
    
    # Label encoding floor
    encoding = file['floor_label_encoder_file']
    lab_encoded_floor = encoding.transform(y_train['FLOOR']).reshape(-1, 1)
    
    y_train_temp['FLOOR'] = lab_encoded_floor
    
    # Label encoding building
    encoding_building = file['building_label_encoder_file']
    lab_encoded_building = encoding_building.transform(y_train['BUILDINGID'])
    
    y_train_temp['BUILDINGID'] = lab_encoded_floor
    
    # Data cleansing
    X_train, y_train = clean_dataset(org_x_train=file['x_data_original_file'], org_y_train=file['y_data_original_file'],
                                     preprocessed_x_train=x_train_preprocessed, threshold=params['threshold'])
    
    fingerprints_removed = np.shape(file['x_data_original_file'])[0] - np.shape(X_train)[0]
    
    insert_data(collection_id=data_cleansing, id=uuid_file, 
                    parameter='result.removed_fingerprints', value=str(fingerprints_removed), 
                    path_file='')
    
    # Save the X training set
    file_x_training_set = os.path.join(temp_path, uuid_file + '_X_TRAIN_SET' + '.save')
    joblib.dump(X_train, file_x_training_set)
    insert_data(collection_id=config_preproc_id, id=uuid_file, 
                parameter='x_data_original_file', value="", 
                path_file=file_x_training_set)
    # Remove file
    os.remove(file_x_training_set)
    
    # Save the y training set
    file_y_training_set = os.path.join(temp_path, uuid_file + '_Y_TRAIN_SET' + '.save')
    joblib.dump(y_train, file_y_training_set)
    insert_data(collection_id=config_preproc_id, id=uuid_file, 
                parameter='y_data_original_file', value="", 
                path_file=file_y_training_set)
    # Remove file
    os.remove(file_y_training_set)
    
    # create entry to the Dataset table
    insert_dataset(name=params['name'],technique='NONE', process_id=uuid_file)
    
    y_train.columns = ['LONGITUDE','LATITUDE','ALTITUDE','FLOOR','BUILDINGID']
    
    # Test data cleansed
    if params['test']['test_accuracy']== True:
        X_new_train,  y_new_train, X_new_validation, y_new_validation= data_partition(X_train=X_train, y_train=y_train,
                                                                                      test_data_percent=params['test']['percent_test'])
        
        ## Rename Columns
        y_new_train.columns = ['LONGITUDE','LATITUDE','ALTITUDE','FLOOR','BUILDINGID']
        y_new_validation.columns = ['LONGITUDE','LATITUDE','ALTITUDE','FLOOR','BUILDINGID']
        # Label encoding floor
        encoding = file['floor_label_encoder_file']
        lab_encoded_floor_train = encoding.transform(y_new_train['FLOOR']).reshape(-1, 1)
        lab_encoded_floor_validation = encoding.transform(y_new_validation['FLOOR']).reshape(-1, 1)
        
        y_new_train['FLOOR'] = lab_encoded_floor_train
        y_new_validation['FLOOR'] = lab_encoded_floor_validation
        
        # Label encoding building
        encoding_building = file['building_label_encoder_file']
        lab_encoded_building_train = encoding_building.transform(y_new_train['BUILDINGID'])
        lab_encoded_building_validation = encoding_building.transform(y_new_validation['BUILDINGID'])
        
        y_new_train['BUILDINGID'] = lab_encoded_building_train
        y_new_validation['BUILDINGID'] = lab_encoded_building_validation
        
        position = Position_KNN(k=params['test']['k'], metric=params['test']['distance_metric'])
        position.fit(X_new_train, y_new_train.values)
        floor_hit_rate_org, true_false_values_org, pred_fhr_org = position.floor_hit_rate(X_new_validation, y_new_validation.values)
        building_hit_rate_org, pred_bhr_org = position.building_hit_rate(X_new_validation, y_new_validation.values)
        error2D_org, error2D_values_org = position.predict_position_2D(X_new_validation, y_new_validation.values, true_floors=true_false_values_org)
        error3D_org, error3D_values_org = position.predict_position_3D(X_new_validation, y_new_validation.values)
        
        insert_data(collection_id=data_cleansing, id=uuid_file, 
                    parameter='result.mean_3d_error', value=str(round(error3D_org, 2)), 
                    path_file='')
        insert_data(collection_id=data_cleansing, id=uuid_file, 
                    parameter='result.mean_2d_error', value=str(round(error2D_org, 2)), 
                    path_file='')
        insert_data(collection_id=data_cleansing, id=uuid_file, 
                    parameter='result.building_hit_rate', value=str(round(building_hit_rate_org, 2)), 
                    path_file='')
        insert_data(collection_id=data_cleansing, id=uuid_file, 
                    parameter='result.floor_hit_rate', value=str(round(floor_hit_rate_org, 2)), 
                    path_file='')
        
        