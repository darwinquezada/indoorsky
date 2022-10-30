#!/usr/bin/python
from data_partition import data_partition
from sklearn.metrics import confusion_matrix
from appwrite.exception import AppwriteException
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.input_file import InputFile
from appwrite.query import Query
from appwrite.services.storage import Storage
from appwrite.input_file import InputFile
from cnn_lstm import CNN_LSTM
from data_preprocessing import (data_reshape_sample_timestep_feature)

import numpy as np
import pandas as pd
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
bucket_model_id = os.environ['TABLE_FILE']
bucket_preprocessing_id=os.environ['TABLE_FILE_PREPROCESSING']
dataset_id = os.environ['TABLE_DATASET']
data_model = os.environ['TABLE_MODEL']


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
        response = storage.create_file(bucket_id=bucket_model_id, file_id='unique()', file=InputFile.from_path(file_path))
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
        "id_model": id,
        "parameter": parameter,
        "value": value
        }
        
    insert_document(collection_id=collection_id, data=data)



if __name__ == '__main__':
    p = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description='')
    p.add_argument('--params', dest='params', action='store', default='', help='Arguments')
    
    args = p.parse_args()

    params = json.loads(args.params)
    
    # Create a temporal directory to store files
    temp_path = os.path.join(os.getcwd(), 'application', 'temp')
    
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    
    # Unique ID for all files generated
    uuid_file = str(uuid.uuid1())
    
    ################### Save data ###############
    # Save parameters
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='name', value=params['name'], 
                path_file='')
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='dataset_id', value=params['dataset_id'], 
                path_file='')
    # Floor model
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='floor.lr', value=str(params['floor']['lr']), 
                path_file='')
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='floor.epochs', value=str(params['floor']['epochs']), 
                path_file='')
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='floor.batch_size', value=str(params['floor']['batch_size']), 
                path_file='')
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='floor.loss', value=str(params['floor']['loss']), 
                path_file='')
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='floor.optimizer', value=str(params['floor']['optimizer']), 
                path_file='')
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='floor.train', value=str(params['floor']['train']), 
                path_file='')
    # Building model
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='building.lr', value=str(params['building']['lr']), 
                path_file='')
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='building.epochs', value=str(params['building']['epochs']), 
                path_file='')
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='building.batch_size', value=str(params['building']['batch_size']), 
                path_file='')
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='building.loss', value=str(params['building']['loss']), 
                path_file='')
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='building.optimizer', value=str(params['building']['optimizer']), 
                path_file='')
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='building.train', value=str(params['building']['train']), 
                path_file='')
    # Positioning model
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='position.lr', value=str(params['position']['lr']), 
                path_file='')
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='position.epochs', value=str(params['position']['epochs']), 
                path_file='')
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='position.batch_size', value=str(params['position']['batch_size']), 
                path_file='')
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='position.loss', value=str(params['position']['loss']), 
                path_file='')
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='position.optimizer', value=str(params['position']['optimizer']), 
                path_file='')
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='position.train', value=str(params['position']['train']), 
                path_file='')
    # Test data
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='test.test_accuracy', value=str(params['test']['test_accuracy']), 
                path_file='')
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='test.percent_test', value=str(params['test']['percent_test']), 
                path_file='')
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='test.percent_validation', value=str(params['test']['percent_validation']), 
                path_file='')
    
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='is_active', value=str(params['is_active']), 
                path_file='')
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='created_at', value=str(params['created_at']), 
                path_file='')

    #############################################
    
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
            load_file = storage.get_file_view(bucket_preprocessing_id, value)
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
    encoding_floor = file['floor_label_encoder_file']
    lab_encoded_floor = encoding_floor.transform(y_train['FLOOR']).reshape(-1, 1)
    y_train_temp['FLOOR'] = lab_encoded_floor
    
    # One hot encoder floor
    floor_ohe_model = file['floor_one_hot_encoder_file']
    
    # Label encoding building
    encoding_building = file['building_label_encoder_file']
    lab_encoded_building = encoding_building.transform(y_train['BUILDINGID']).reshape(-1, 1)
    y_train_temp['BUILDINGID'] = lab_encoded_building

    # One hot encoder building
    building_ohe_model = file['building_one_hot_encoder_file']
    
    # Latitude normalization
    latitude_norm = file['latitude_normalized_file']
    latitude = latitude_norm.transform(y_train['LATITUDE'].values.reshape(-1, 1))
    y_train_temp['LATITUDE'] = latitude
    
    # Longitude normalization
    longitude_norm = file['longitude_normalized_file']
    longitude = longitude_norm.transform(y_train['LONGITUDE'].values.reshape(-1, 1))
    y_train_temp['LONGITUDE'] = longitude

    # Altitude normalization
    altitude_norm = file['altitude_normalized_file']
    altitude = altitude_norm.transform(y_train['ALTITUDE'].values.reshape(-1, 1))
    y_train_temp['ALTITUDE'] = altitude

    # X_train asigned
    X_train = x_train_preprocessed

    # Generate test set
    X_new_train,  y_new_train, X_new_test, y_new_test = data_partition(X_train=X_train, y_train=y_train_temp,
                                                                      test_data_percent=params['test']['percent_test'])
    # Generate validation set
    X_new_train,  y_new_train, X_new_validation, y_new_validation = data_partition(X_train=X_new_train, y_train=y_new_train,
                                                                      test_data_percent=params['test']['percent_validation'])

    # Floor one hot encoding
    floor_one_hot_encoder_train = floor_ohe_model.transform(y_new_train['FLOOR'].values.reshape(-1, 1))
    floor_one_hot_encoder_test = floor_ohe_model.transform(y_new_test['FLOOR'].values.reshape(-1, 1))
    floor_one_hot_encoder_validation = floor_ohe_model.transform(y_new_validation['FLOOR'].values.reshape(-1, 1))

    # Building one hot encoding
    building_one_hot_encoder_train = building_ohe_model.transform(y_new_train['BUILDINGID'].values.reshape(-1, 1))
    building_one_hot_encoder_test = building_ohe_model.transform(y_new_test['BUILDINGID'].values.reshape(-1, 1))
    building_one_hot_encoder_validation = building_ohe_model.transform(y_new_validation['BUILDINGID'].values.reshape(-1, 1))

    X_data = {}
    y_data = {}

    X_data['X_train'] = X_new_train.values
    X_data['X_test'] = X_new_test.values
    X_data['X_validation'] = X_new_validation.values

    y_data['y_train'] = {}

    y_data['y_train']['position'] = y_new_train.iloc[:,0:3]
    y_data['y_train']['floor'] = floor_one_hot_encoder_train
    y_data['y_train']['building'] = building_one_hot_encoder_train

    y_data['y_test'] = {}

    y_data['y_test']['position'] = y_new_test.iloc[:,0:3]
    y_data['y_test']['floor'] = floor_one_hot_encoder_test
    y_data['y_test']['building'] = building_one_hot_encoder_test

    y_data['y_validation'] = {}

    y_data['y_validation']['position'] = y_new_validation.iloc[:,0:3]
    y_data['y_validation']['floor'] = floor_one_hot_encoder_validation
    y_data['y_validation']['building'] = building_one_hot_encoder_validation

    cnn_lstm_model = CNN_LSTM(X_data=X_data, y_data=y_data, 
                              building_config=params['building'], 
                              floor_config=params['floor'],
                              position_config=params['position'])

    positioning_model, floor_model, building_model = cnn_lstm_model.train()

    # Save positioning model
    file_positioning_model = os.path.join(temp_path, uuid_file + '_POSITIONING_MODEL.save')
    joblib.dump(positioning_model,file_positioning_model,compress=True)
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='positioning_model', value="", 
                path_file=file_positioning_model)
    # Remove file
    os.remove(file_positioning_model)

    # Save floor model
    file_floor_model = os.path.join(temp_path, uuid_file + '_FLOOR_MODEL.save')
    joblib.dump(floor_model, file_floor_model, compress=True)
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='floor_model', value="", 
                path_file=file_floor_model)
    # Remove file
    os.remove(file_floor_model)

    # Save floor model
    file_building_model = os.path.join(temp_path, uuid_file + '_BUILDING_MODEL.save')
    joblib.dump(building_model,file_building_model, compress=True)
    insert_data(collection_id=data_model, id=uuid_file, 
                parameter='building_model', value="", 
                path_file=file_building_model)
    # Remove file
    os.remove(file_building_model)

    # Test data cleansed
    if params['test']['test_accuracy']== True:
        # Reshape test data
        X_test = data_reshape_sample_timestep_feature(X_new_test)
        # Predict Building
        predicted_bld = building_model.predict(X_test)
        predicted_bld = np.argmax(predicted_bld, axis=-1)
        subs_pred_test_building = np.subtract(predicted_bld, y_new_test['BUILDINGID'])
        building_hit_rate = (sum(map(lambda x: x == 0, subs_pred_test_building))/np.shape(y_new_test['BUILDINGID'])[0])*100
        predicted_bld = encoding_building.inverse_transform(predicted_bld)

        # Predict floor
        predicted_floor = floor_model.predict(X_test)
        predicted_floor = np.argmax(predicted_floor, axis=-1)
        subs_pred_test_floor = np.subtract(predicted_floor, y_new_test['FLOOR'])
        floor_hit_rate = (sum(map(lambda x: x == 0, subs_pred_test_floor))/np.shape(y_new_test['FLOOR'])[0])*100
        predicted_floor = encoding_floor.inverse_transform(predicted_floor)

        # Predict position
        predict_position = positioning_model.predict(X_test)

        predict_long = longitude_norm.inverse_transform(predict_position[:, 0].reshape(-1, 1))
        predict_lat = latitude_norm.inverse_transform(predict_position[:, 1].reshape(-1, 1))
        predict_alt = altitude_norm.inverse_transform(predict_position[:, 2].reshape(-1, 1))

        predict_long = np.reshape(predict_long[:], (1, len(predict_long[:, 0])))
        predict_lat = np.reshape(predict_lat[:], (1, len(predict_lat[:, 0])))
        predict_alt = np.reshape(predict_alt[:], (1, len(predict_alt[:, 0])))

        test_long = longitude_norm.inverse_transform(y_new_test['LONGITUDE'].values.reshape(-1, 1))
        test_lat = latitude_norm.inverse_transform(y_new_test['LATITUDE'].values.reshape(-1, 1))
        test_alt = altitude_norm.inverse_transform(y_new_test['ALTITUDE'].values.reshape(-1, 1))

        test_long = np.reshape(test_long[:], (1, len(test_long[:, 0])))
        test_lat = np.reshape(test_lat[:], (1, len(test_lat[:, 0])))
        test_alt = np.reshape(test_alt[:], (1, len(test_alt[:, 0])))

        df_prediction = pd.DataFrame(list(zip(predict_long[0][:], predict_lat[0][:], predict_alt[0][:])),
                                     columns=['LONGITUDE', 'LATITUDE', 'ALTITUDE'])

        df_test = pd.DataFrame(list(zip(test_long[0][:], test_lat[0][:], test_alt[0][:])),
                               columns=['LONGITUDE', 'LATITUDE', 'ALTITUDE'])

        error_2d = np.linalg.norm(df_prediction.iloc[:, 0:2].values - df_test.iloc[:, 0:2].values, axis=1)
        mean_2d_error = np.mean(error_2d)

        error_3d = np.linalg.norm(df_prediction.iloc[:, 0:3].values - df_test.iloc[:, 0:3].values, axis=1)
        mean_3d_error = np.mean(error_3d)

        insert_data(collection_id=data_model, id=uuid_file,
                    parameter='result.mean_3d_error', value=str(round(mean_3d_error, 2)),
                    path_file='')
        insert_data(collection_id=data_model, id=uuid_file,
                    parameter='result.mean_2d_error', value=str(round(mean_2d_error, 2)),
                    path_file='')
        insert_data(collection_id=data_model, id=uuid_file,
                    parameter='result.building_hit_rate', value=str(round(building_hit_rate, 2)),
                    path_file='')
        insert_data(collection_id=data_model, id=uuid_file,
                    parameter='result.floor_hit_rate', value=str(round(floor_hit_rate, 2)),
                    path_file='')
        insert_data(collection_id=data_model, id=uuid_file,
                    parameter='status',value='completed',
                    path_file='')