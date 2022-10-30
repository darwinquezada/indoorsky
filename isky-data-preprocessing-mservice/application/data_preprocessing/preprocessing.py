#!/usr/bin/python
from importlib.resources import path
import os
import time
import json
import argparse
import uuid
from appwrite.exception import AppwriteException
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.input_file import InputFile
from appwrite.services.storage import Storage
from appwrite.input_file import InputFile
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, Normalizer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from data_representation import DataRepresentation
from data_preprocessing import new_non_detected_value

from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from dotenv import load_dotenv
from datetime import datetime
from numpy.random import seed, default_rng
from subprocess import PIPE, Popen, STDOUT
import pandas as pd
import numpy as np
import joblib
import time as ti

from datetime import datetime
import time

### Warning ###
import warnings
from flask import jsonify

warnings.filterwarnings('ignore')

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)

r = RethinkDB()

client = Client()
client.set_endpoint(os.environ['APPWRITEENDPOINT'])
client.set_project(os.environ['APPWRITEPROJECTID'])
client.set_key(os.environ['APPWRITEAPIKEY'])


database_id = os.environ['RDB_DB']
config_preproc_id = os.environ['TABLE_PREPROCESSING']
bucket_preproc_id = os.environ['TABLE_FILE']
dataset_id = os.environ['TABLE_DATASET']


def connection():
    # Database connection RethinkDB
    try:
        conn = r.connect(host=os.environ['RDB_HOST'],  port=os.environ['RDB_PORT'])
        return conn
    except RqlRuntimeError as e:
        return jsonify({'code': '0', 'message': e.message})

def get_technology(conn, pos_tech_id: str):
    try:
        technology = r.db(os.environ['RDB_DB']).table('pos_technology').get(pos_tech_id).to_json().run(conn)
        tech_name = json.loads(technology)['code']

        if tech_name == '':
            return False
        return tech_name
    except RqlDriverError as e:
        return jsonify({'code':501, 'message':e})

def insert_document(collection_id: str, data: dict):
    try:
        databases = Databases(client)
        response = databases.create_document(database_id=database_id, collection_id=collection_id,
                                             document_id='unique()', data=data)
        return response['$id']
    except AppwriteException as e:
        print({'code': '0', 'message': e.message})

def upload_file(file_path:str):
    try:
        storage = Storage(client)
        response = storage.create_file(bucket_id=bucket_preproc_id, file_id='unique()', file=InputFile.from_path(file_path))
        return response['$id']
    except AppwriteException as e:
        print({'code': '0', 'message': e.message})

def insert_data(collection_id: str, id:str, parameter: str, value: str, path_file: str):

    if path_file != "":
        file_id = upload_file(path_file)
        value = file_id

    data = {
        "id_preprocessing": id,
        "parameter": parameter,
        "type": "PREPROCESSING",
        "value": value
        }
    insert_document(collection_id=collection_id, data=data)

def insert_dataset(name:str, technique: str, process_id: str):
    data = {
        "name": name,
        "technique": technique,
        "type": "PREPROCESSING",
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

    # Data
    tech_id = params['pos_tech_id']
    date_start = params['date_start']
    date_end =  params['date_end']
    env_id = params['env_id']
    building_id = params['building_id']
    floor_id = params['floor_id']
    non_detected_value = params['non_dected_value']

    # Instances
    databases = Databases(client)
    storage = Storage(client)

    # Create a temporal directory to store files
    temp_path = os.path.join(os.getcwd(), 'application', 'temp')

    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    # Unique ID for all files generated during the preprocessing
    uuid_file = str(uuid.uuid1())

    # Insert data
    document_id = str(uuid.uuid1())
    
    insert_data(collection_id=config_preproc_id, id=document_id,
                parameter='name', value=params['name'],
                path_file="")
    insert_data(collection_id=config_preproc_id, id=document_id,
                parameter='pos_tech_id', value=params['pos_tech_id'],
                path_file="")
    insert_data(collection_id=config_preproc_id, id=document_id,
                parameter='env_id', value=params['env_id'],
                path_file="")
    if params['building_id']!="":
        insert_data(collection_id=config_preproc_id, id=document_id,
                parameter='building_id', value=params['building_id'],
                path_file="")
    if params['floor_id']!="":
        insert_data(collection_id=config_preproc_id, id=document_id,
                parameter='floor_id', value=params['floor_id'],
                path_file="")
    insert_data(collection_id=config_preproc_id, id=document_id,
                parameter='non_dected_value', value=str(params['non_dected_value']),
                path_file="")
    
    # RethinkDB connection
    conn = connection()

    # Technology
    technology = r.db(database_id).table('pos_technology').get(tech_id).to_json().run(conn)
    tech_name = json.loads(technology)['code']

    # Get POIs
    """
    pois = r.db(database_id).table('fingerprint').filter(
            (r.row['env_id'] == env_id) &
            (r.row['created_at'] >= date_start) &
            (r.row['created_at'] <= date_end)).concat_map(
                    lambda fingerprint: r.db(database_id).table('poi').get_all(
                        fingerprint['poi_id'], index='id'
                    ).map(
                        lambda poi: { 'left': fingerprint, 'right': poi}
                    )).zip().run(conn)
    """
    list_pois = r.db(database_id).table('poi').run(conn)
    df_list_poi = pd.DataFrame.from_dict(list_pois)
    df_list_poi = df_list_poi.rename(columns={'id':'poi_id'})
    
    list_fingerprints = r.db(database_id).table('fingerprint').filter(
            (r.row['env_id'] == env_id) &
            (r.row['created_at'] >= date_start) &
            (r.row['created_at'] <= date_end)).run(conn)
    df_list_fingerprints = pd.DataFrame.from_dict(list_fingerprints).copy()
    
    # Merge POIs and Fingerprints based on the poi_id
    df_fingerprints_pois = df_list_fingerprints.merge(df_list_poi, how='left', on='poi_id')
    
    """
    pois = r.db(database_id).table('fingerprint').filter(
            (r.row['env_id'] == env_id) &
            (r.row['created_at'] >= date_start) &
            (r.row['created_at'] <= date_end)).concat_map(
                    lambda fingerprint: r.db(database_id).table('poi').get_all(
                        fingerprint['poi_id'], index='id'
                    ).map(
                        lambda poi: { 'left': fingerprint, 'right': poi}
                    )).zip().run(conn)
            
    df_poi = pd.DataFrame.from_dict(pois).copy()
    """
    df_fingerprints_selected_columns = df_fingerprints_pois[['id', 'longitude', 'latitude', 'altitude', 'building_id', 'floor_id_x']].copy()
    # df_fingerprints_selected_columns = df_fingerprints_pois[['id', 'longitude', 'latitude', 'altitude','floor_id_x','building_id']].copy()
    # Remove this
    df_fingerprints_selected_columns = df_fingerprints_selected_columns.rename(columns={'id':'fingerprint_id', 'building_id': 'floor_id', 
                                                                                        'floor_id_x':'building_id' })

    # Get fingerprints
    measurements = r.db(database_id).table('fingerprint').filter(
                    (r.row['env_id'] == env_id) &
                    (r.row['created_at'] >= date_start) &
                    (r.row['created_at'] <= date_end)).concat_map(
                    lambda fingerprint: r.db(database_id).table(tech_name + '_fingerprint').get_all(
                        fingerprint['id'], index='fingerprint_id'
                    ).map(
                        lambda measurement: { 'left': fingerprint, 'right': measurement}
                    )).zip().run(conn)

    df_measurements = pd.DataFrame.from_dict(measurements).set_index('fingerprint_id')

    # Fingerprit table
    piv_df = pd.pivot_table(df_measurements, values='rssi', index=['fingerprint_id'],
                    columns=['bssid'], fill_value=non_detected_value).reset_index()
    
    unique_aps = piv_df.columns
    
    # Save the file in the temporal directory
    file_aps = os.path.join(temp_path, uuid_file + '_APS' + '.save')
    joblib.dump(unique_aps, file_aps, compress=True)
    insert_data(collection_id=config_preproc_id, id=document_id,
                parameter='list_aps_file', value='',
                path_file=file_aps)
    # Remove file
    os.remove(file_aps)
    
    # Get len unique APs
    len_unique_aps = len(unique_aps)
    # Merge fingerprints data with measurements
    df_merge = piv_df.merge(df_fingerprints_selected_columns, how='left', on='fingerprint_id')
    
    # Traning set
    X_train = df_merge.iloc[:,1:len_unique_aps]

    # Labels training set
    y_train = df_merge[['longitude', 'latitude', 'altitude', 'floor_id', 'building_id']].copy()

    # Train dataset
    train_data = pd.concat([X_train, y_train], axis=1)

    # Save the X training set
    file_x_training_set = os.path.join(temp_path, uuid_file + '_X_TRAIN_SET' + '.save')
    joblib.dump(X_train, file_x_training_set, compress=True)
    insert_data(collection_id=config_preproc_id, id=document_id,
                parameter='x_data_original_file', value="",
                path_file=file_x_training_set)
    # Remove file
    os.remove(file_x_training_set)

    # Save the y training set
    file_y_training_set = os.path.join(temp_path, uuid_file + '_Y_TRAIN_SET' + '.save')
    joblib.dump(y_train, file_y_training_set, compress=True)
    insert_data(collection_id=config_preproc_id, id=document_id,
                parameter='y_data_original_file', value="",
                path_file=file_y_training_set)
    # Remove file
    os.remove(file_y_training_set)

    # create entry to the Dataset table
    insert_dataset(name=params['name'],technique='NONE', process_id=document_id)

    # Change data representation
    if params['data_representation'] != 'none':
        insert_data(collection_id=config_preproc_id, id=document_id,
                parameter='data_representation', value=params['data_representation'],
                path_file='')

        # create entry to the Dataset table
        insert_dataset(name=params['name'],technique='TRANSFORMATION', process_id=document_id)

        new_non_det_val = new_non_detected_value(X_train)

        insert_data(collection_id=config_preproc_id, id=document_id,
                parameter='new_non_detected_value', value=str(new_non_det_val),
                path_file='')

        dr = DataRepresentation(x_train=X_train,
                                type_rep=params['data_representation'],
                                def_no_val=params['non_dected_value'],
                                new_no_val=new_non_det_val)

        X_train = dr.data_rep()
        file_data_transformed = os.path.join(temp_path, uuid_file + '_DATA_TRANSFORMED' + '.save')
        joblib.dump(X_train, file_data_transformed, compress=True)
        insert_data(collection_id=config_preproc_id, id=document_id,
                    parameter='x_data_transformed_file', value='',
                    path_file=file_data_transformed)
        # Remove file
        os.remove(file_data_transformed)

    if params['x_normalization']!='none':
        insert_data(collection_id=config_preproc_id, id=document_id,
                    parameter='x_technique_normalization',
                    value=params['x_normalization'],
                    path_file='')

        insert_dataset(name=params['name'],technique='NORMALIZATION', process_id=document_id)

        if params['x_normalization'] == 'minmax':
            normalization = MinMaxScaler()
        elif params['x_normalization'] == 'standard':
            normalization = StandardScaler()
        elif params['x_normalization'] == 'robust':
            normalization = RobustScaler()
        elif params['x_normalization'] == 'normalizer':
            normalization = Normalizer()
        else:
            pass

        X_train = normalization.fit_transform(X_train)
        file_x_norm = os.path.join(temp_path, uuid_file + '_X_NORM' + '.save')
        joblib.dump(normalization, file_x_norm, compress=True)
        insert_data(collection_id=config_preproc_id, id=document_id,
                    parameter='x_model_normalization_file', value='',
                    path_file=file_x_norm)
        # Remove file
        os.remove(file_x_norm)

        file_x_data_norm = os.path.join(temp_path, uuid_file + '_X_DATA_NORM' + '.save')
        joblib.dump(X_train, file_x_data_norm, compress=True)
        insert_data(collection_id=config_preproc_id, id=document_id,
                    parameter='x_data_normalization_file', value='',
                    path_file=file_x_data_norm)
        # Remove file
        os.remove(file_x_data_norm)

    # Encoding floor
    encoding = LabelEncoder()
    lab_encoded_floor = encoding.fit_transform(y_train['floor_id'])
    floor_labelencoder_file = os.path.join(temp_path, uuid_file + '_FLOOR_LABEL_ENCODER' + '.save')
    joblib.dump(encoding, floor_labelencoder_file, compress=True)
    insert_data(collection_id=config_preproc_id, id=document_id,
                parameter='floor_label_encoder_file', value='',
                path_file=floor_labelencoder_file)
    os.remove(floor_labelencoder_file)

    onehot_encoder_floor = OneHotEncoder(sparse=False)
    floor_one_hot_encoder = onehot_encoder_floor.fit_transform(lab_encoded_floor.reshape(-1, 1))
    floor_one_hot_encoder_file = os.path.join(temp_path, uuid_file + '_FLOOR_ONE_HOT_ENCODER' + '.save')
    joblib.dump(onehot_encoder_floor, floor_one_hot_encoder_file, compress=True)
    insert_data(collection_id=config_preproc_id, id=document_id,
                parameter='floor_one_hot_encoder_file', value='',
                path_file=floor_one_hot_encoder_file)
    os.remove(floor_one_hot_encoder_file)

    # Encoding building
    encoding_building = LabelEncoder()
    lab_encoded_building = encoding_building.fit_transform(y_train['building_id'])
    building_labelencoder_file = os.path.join(temp_path, uuid_file + '_BUILDING_LABEL_ENCODER' + '.save')
    joblib.dump(encoding_building, building_labelencoder_file, compress=True)
    insert_data(collection_id=config_preproc_id, id=document_id,
                parameter='building_label_encoder_file', value='',
                path_file=building_labelencoder_file)
    os.remove(building_labelencoder_file)

    onehot_encoder_building = OneHotEncoder(sparse=False)
    building_one_hot_encoder = onehot_encoder_building.fit_transform(lab_encoded_building.reshape(-1, 1))
    building_one_hot_encoder_file = os.path.join(temp_path, uuid_file + '_BUILDING_ONE_HOT_ENCODER' + '.save')
    joblib.dump(onehot_encoder_building, building_one_hot_encoder_file, compress=True)
    insert_data(collection_id=config_preproc_id, id=document_id,
                parameter='building_one_hot_encoder_file', value='',
                path_file=building_one_hot_encoder_file)
    os.remove(building_one_hot_encoder_file)

    # Latitude, longitude and altitude normalization
    if params['y_normalization'] != "":
        insert_data(collection_id=config_preproc_id, id=document_id,
                    parameter='y_technique_normalization',
                    value=params['y_normalization'],
                    path_file='')

        if params['x_normalization'] == 'minmax':
            normalization = MinMaxScaler()
        elif params['x_normalization'] == 'stardard':
            normalization = StandardScaler()
        elif params['x_normalization'] == 'robust':
            normalization = RobustScaler()
        elif params['x_normalization'] == 'normalizer':
            normalization = Normalizer()
        else:
            pass

        # Scale longitude
        scaled_long = normalization
        long_y_train = scaled_long.fit_transform(y_train['longitude'].values.reshape(-1, 1))
        scaled_long_file = os.path.join(temp_path, uuid_file + '_LONGITUDE_NORMALIZED' + '.save')
        joblib.dump(scaled_long, scaled_long_file, compress=True)
        insert_data(collection_id=config_preproc_id, id=document_id,
                    parameter='longitude_normalized_file', value='',
                    path_file=scaled_long_file)
        os.remove(scaled_long_file)

        # Scale Latitude
        scaled_lat = normalization
        lat_y_train = scaled_lat.fit_transform(y_train['latitude'].values.reshape(-1, 1))
        scaled_lat_file = os.path.join(temp_path, uuid_file + '_LATITUDE_NORMALIZED' + '.save')
        joblib.dump(scaled_lat, scaled_lat_file, compress=True)
        insert_data(collection_id=config_preproc_id, id=document_id,
                    parameter='latitude_normalized_file', value='',
                    path_file=scaled_lat_file)
        os.remove(scaled_lat_file)

        # Scale Altitude
        scaled_alt = MinMaxScaler()
        alt_y_train = scaled_alt.fit_transform(y_train['altitude'].values.reshape(-1, 1))
        scaled_alt_file = os.path.join(temp_path, uuid_file + '_ALTITUDE_NORMALIZED' + '.save')
        joblib.dump(scaled_alt, scaled_alt_file, compress=True)
        insert_data(collection_id=config_preproc_id, id=document_id,
                    parameter='altitude_normalized_file', value='',
                    path_file=scaled_alt_file)
        os.remove(scaled_alt_file)

        # Status
        millisecond = datetime.now()
        created= time.mktime(millisecond.timetuple()) * 1000

        insert_data(collection_id=config_preproc_id, id=document_id,
                    parameter='created_at',
                    value=str(created),
                    path_file='')
        insert_data(collection_id=config_preproc_id, id=document_id,
                    parameter='status',
                    value='completed',
                    path_file='')
