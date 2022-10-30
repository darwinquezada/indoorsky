import shutil
from statistics import mode
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
from appwrite.exception import AppwriteException
from appwrite.query import Query
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, Normalizer
from application.data.data_source.positioning_datasource import IPositioningDatasource
from application.core.exceptions.status_codes import (SuccessResponseCode,
                                                      NotFoundResponseCode,
                                                      ConflictResponseCode,
                                                      AcceptedResponseCode,
                                                      InternalServerErrorResponseCode)
from application.algorithm.data_representation import DataRepresentation
from application.algorithm.data_preprocessing import new_non_detected_value, data_reshape_sample_timestep_feature
from tensorflow.keras.models import load_model
from application.algorithm.elm import elmTrain_fix, elmPredict_optim
from application.algorithm.cnn import convlayer
import keras.backend as K
import numpy as np
from flask import jsonify
from datetime import datetime
import pandas as pd
import time
import json
import os
from io import BytesIO
import joblib

class PositioningDatasourceImpl(IPositioningDatasource):
    def __init__(self, client: Client, database_name: str, tables: dict) -> None:
        self.database_name = database_name
        self.tables = tables
        self.client = client

    def get_position(self, pos_tech_id:str, model_type:str, data: json) -> dict:
        try:
            path = os.path.join(os.getcwd(), 'application', 'models', pos_tech_id,model_type)
            
            if not os.path.exists(os.path.join(path)):
                return NotFoundResponseCode(message="Model not found.")
            # Load list of APS
            list_aps_file = joblib.load(os.path.join(path,'list_aps_file.save'))
            aps = list_aps_file[1:]
            
            # Loading the config file
            config_file = joblib.load(os.path.join(path,'config.save'))
            
            # Convert list of APs to DataFrame
            df_aps = pd.DataFrame(columns=aps)
            incoming_fingerprints = {}
            for measurement in data:
                if measurement.bssid in aps:
                    incoming_fingerprints[measurement.bssid] = float(measurement.rss)

            df_aps = df_aps.append(incoming_fingerprints, ignore_index=True).fillna(float(config_file['preprocessing_config']['non_dected_value']))
            
            estimation = self.process_fingerprint(df_aps, config_file, path)
            
            return jsonify(estimation)

        except AppwriteException as e:
            return InternalServerErrorResponseCode(message=e.message)

    def set_models(self, model: json) -> dict:
        """
        Set the default positioning models (positioning, building, floor)
        Parameters:
        model: model information json (model, model type, positioning technology ID aand data model ID)
        Return:
        status: 200 OK
        """
        try:
            # Instanciate the datastore and storage
            storage = Storage(self.client)
            databases = Databases(self.client)

            # Create a temporal directory to store files
            temp_path = os.path.join(os.getcwd(), 'application', 'models', model['pos_tech_id'],
                                     model['model_type'])
            
            # Create the directory to store the models
            if not os.path.exists(temp_path):
                os.makedirs(temp_path)

            # Chech if there is a register with the same parameters
            # Only of POSITONING, FLOOR and BUILDING are allowed
            document_model = databases.list_documents(self.database_name, self.tables['model'],
                                              queries=[Query.equal('model', model['model']),
                                                       Query.equal('model_type', model['model_type']),
                                                       Query.equal('pos_tech_id', model['pos_tech_id']),
                                                       Query.equal('data_model_id', model['data_model_id'])])

            if document_model['total'] == 0:

                document_data_model = databases.list_documents(self.database_name, self.tables['data_model'],
                                              queries=[Query.equal('id_model', model['data_model_id']),
                                                       Query.limit(100)])
                
                data_model = {}
                
                if document_data_model['total'] == 0:
                    return NotFoundResponseCode(message="Data model ID not found.")

                for document in document_data_model['documents']:
                    data_model[document['parameter']] = document['value']
                    param_names = document['parameter'].split('_')

                    if model['model'] == "CNN-LSTM":
                        if param_names[0].upper() == model['model_type']:
                            load_file = storage.get_file_view(self.tables['file_model'], document['value'])
                            file_tranform = BytesIO(load_file)
                            file = joblib.load(file_tranform)
                            joblib.dump(file,os.path.join(temp_path, model['model_type']+'.save'))
                    else:
                        if param_names[-1] == 'file':
                            load_file = storage.get_file_view(self.tables['file_model'], document['value'])
                            file_tranform = BytesIO(load_file)
                            file = joblib.load(file_tranform)
                            joblib.dump(file, os.path.join(temp_path, document['parameter']+'.save'))
                            
                    if document['parameter'] == 'dataset_id':
                        dataset = databases.get_document(self.database_name, self.tables['dataset'],
                                                                  document['value'])
                        
                        preprocessing_files = databases.list_documents(self.database_name, self.tables['preprocessing'],
                                              queries=[Query.equal('id_preprocessing', dataset['process_id']),
                                                       Query.limit(100)])

                        preprocessing_config = {}
                        for parameters in preprocessing_files['documents']:
                            preprocessing_config[parameters['parameter']] = parameters['value']
                            parameter = parameters['parameter'].split('_')
                            if not 'data' in parameter:
                                if  parameter[-1] == 'file':
                                    load_file = storage.get_file_view(self.tables['file_preprocessing'], parameters['value'])
                                    file_tranform = BytesIO(load_file)
                                    file_object = joblib.load(file_tranform)
                                    joblib.dump(file_object, os.path.join(temp_path, parameters['parameter']+'.save'))
                        
                        
                # Save configuration file
                config = {
                        'model': model,
                        'data_model': data_model,
                        'dataset_config': dataset,
                        'preprocessing_config': preprocessing_config
                    }
                        
                joblib.dump(config, os.path.join(temp_path, 'config.save'))
                
                # Save model
                response = databases.create_document(database_id=self.database_name, collection_id=self.tables['model'],
                                                document_id='unique()', data=model)

                return SuccessResponseCode()
            return ConflictResponseCode(message="There is a register with the same parameters.")
        except AppwriteException as e:
            return InternalServerErrorResponseCode(message=e.message)

    def delete_set_model(self, set_model_id: str) -> dict:
        try:
            databases = Databases(self.client)
            model = databases.get_document(self.database_name, self.tables['model'], set_model_id)
            remove_document = databases.delete_document(self.database_name, self.tables['model'], set_model_id)
            
            path = os.path.join(os.getcwd(), 'application', 'models', model['pos_tech_id'], model['model_type'])
            
            if os.path.exists(path):    
                shutil.rmtree(path)
                
            return SuccessResponseCode()

        except AppwriteException as e:
            return InternalServerErrorResponseCode(message=e.message)

    def update_set_model(self, set_model_id: str, model: json) -> dict:

        return super().update_set_model(set_model_id, model)

    def get_set_model_by_model_type(self, model_type: str) -> dict:
        try:
            databases = Databases(self.client)
            model = databases.list_documents(self.database_name, self.tables['model'],
                                              queries=[Query.equal('model_type', model_type)])
            return model
        except AppwriteException as e:
            return InternalServerErrorResponseCode(message=e.message)
        
    def wrapper(self, func, arg, arg2, queue):
        queue.put(func(arg, arg2))
            
    def process_fingerprint(self, fingerprint, config_file, path):
        
        # Change data representation
        if config_file['preprocessing_config']['data_representation'] != 'none':
            
            new_non_det_val = float(config_file['preprocessing_config']['new_non_detected_value'])

            dr = DataRepresentation(x_train=fingerprint.values,
                                    type_rep=config_file['preprocessing_config']['data_representation'],
                                    def_no_val=float(config_file['preprocessing_config']['non_dected_value']),
                                    new_no_val=new_non_det_val)

            X_train = dr.data_rep()

        if config_file['dataset_config']['technique']!='TRANSFORMATION':

            if config_file['preprocessing_config']['x_technique_normalization'] == 'minmax':
                normalization = MinMaxScaler()
            elif config_file['preprocessing_config']['x_technique_normalization'] == 'standard':
                normalization = StandardScaler()
            elif config_file['preprocessing_config']['x_technique_normalization'] == 'robust':
                normalization = RobustScaler()
            elif config_file['preprocessing_config']['x_technique_normalization'] == 'normalizer':
                normalization = Normalizer()
            else:
                pass

            X_train = normalization.fit_transform(fingerprint)
            
        if config_file['model']['model_type'] == 'POSITIONING':
            estimation = self.estimate_position(X_train, path)
        elif config_file['model']['model_type'] == 'FLOOR':
            if config_file['model']['model'] == 'CNN-LSTM':
                estimation = self.estimate_floor_cnn_lstm(X_train, path)
            else:
                estimation = self.estimate_floor_cnn_elm(X_train, config_file, path)
        else:
            if config_file['model']['model'] == 'CNN-LSTM':
                estimation = self.estimate_building_cnn_lstm(X_train, path)
            else:
                estimation = self.estimate_building_cnn_elm(X_train, config_file, path)
            
        
        return estimation
            
        
    def estimate_position(self, data, path):
        # Reshape data
        X_train = data_reshape_sample_timestep_feature(data)
        
        # Load models
        positioning_model = joblib.load(os.path.join(path,'POSITIONING.save'))
        norm_lon = joblib.load(os.path.join(path,'longitude_normalized_file.save'))
        norm_lat = joblib.load(os.path.join(path,'latitude_normalized_file.save'))
        norm_alt = joblib.load(os.path.join(path,'altitude_normalized_file.save'))
        
        # Estimate the user position
        predict_position = positioning_model.predict(X_train)

        predict_long = norm_lon.inverse_transform(predict_position[:, 0].reshape(-1, 1))
        predict_lat = norm_lat.inverse_transform(predict_position[:, 1].reshape(-1, 1))
        predict_alt = norm_alt.inverse_transform(predict_position[:, 2].reshape(-1, 1))
        
        position = {
            'longitude': float(predict_long[0][0]),
            'latitude': float(predict_lat[0][0]),
            'altitude': float(predict_alt[0][0])
        }
        return position
    
    def estimate_floor_cnn_lstm(self, data, path):
        # Reshape data
        X_train = data_reshape_sample_timestep_feature(data)
        
        # Load models
        floor_model = joblib.load(os.path.join(path,'FLOOR.save'))
        floor_encoder_model = joblib.load(os.path.join(path,'floor_label_encoder_file.save'))
        # Predict floor
        predicted_floor = floor_model.predict(X_train)
        predicted_floor = floor_encoder_model.inverse_transform(np.argmax(predicted_floor, axis=-1))
        
        floor = {
            'floor_id': str(predicted_floor[0])
        }
        return floor
    
    def estimate_building_cnn_lstm(self, data, path):
        # Reshape data
        X_train = data_reshape_sample_timestep_feature(data)
        
        # Load models
        building_model = joblib.load(os.path.join(path,'BUILDING.save'))
        building_encoder_model = joblib.load(os.path.join(path,'building_label_encoder_file.save'))
        # Predict floor
        predicted_building = building_model.predict(X_train)
        predicted_building = building_encoder_model.inverse_transform(np.argmax(predicted_building, axis=-1))
        
        building = {
            'building_id': str(predicted_building[0])
        }
        return building
    
    def estimate_floor_cnn_elm(self, data, config, path):
        cnn = {
            "padding":config["data_model"]["cnn.padding"],
            "strides":int(config["data_model"]["cnn.strides"]),
            "data_format":config["data_model"]["cnn.data_format"],
            "act_funct":config["data_model"]["cnn.act_funct"],
            "kernel_size":int(config["data_model"]["cnn.kernel_size"]),
            "filter":int(config["data_model"]["cnn.filter"])
        }
        
        X_test = data.reshape((data.shape[0], data.shape[1], 1))
        
        # Training Models
        X_test = X_test.astype('float32')
        intest = K.variable(X_test)
        
        out_test_ = convlayer(intest, cnn_config=cnn)
        
        out_test = K.eval(out_test_)
        K.clear_session()  # to avoid overloads
        
        SamplesTest = out_test.T
        
        # Load weights
        floor_output_weights = joblib.load(os.path.join(path,'floor_output_weights_file.save'))
        floor_input_weights = joblib.load(os.path.join(path,'floor_input_weights_file.save'))
        
        # Load models
        floor_encoder_model = joblib.load(os.path.join(path,'floor_label_encoder_file.save'))
        
        # Prediction
        scores, h_test = elmPredict_optim(SamplesTest, floor_input_weights, floor_output_weights, config["data_model"]["elm.act_funct"])

        # Floor prediction
        predicted_floor = floor_encoder_model.inverse_transform(np.argmax(np.transpose(scores), axis=-1))
        
        floor = {
            'floor_id': str(predicted_floor[0])
        }
        return floor
    
    def estimate_building_cnn_elm(self, data, config, path):
        cnn = {
            "padding":config["data_model"]["cnn.padding"],
            "strides":int(config["data_model"]["cnn.strides"]),
            "data_format":config["data_model"]["cnn.data_format"],
            "act_funct":config["data_model"]["cnn.act_funct"],
            "kernel_size":int(config["data_model"]["cnn.kernel_size"]),
            "filter":int(config["data_model"]["cnn.filter"])
        }
        
        X_test = data.reshape((data.shape[0], data.shape[1], 1))
        
        # Training Models
        X_test = X_test.astype('float32')
        intest = K.variable(X_test)
        
        out_test_ = convlayer(intest, cnn_config=cnn)
        
        out_test = K.eval(out_test_)
        K.clear_session()  # to avoid overloads
        
        SamplesTest = out_test.T
        
        # Load weights
        
        building_input_weights = joblib.load(os.path.join(path,'building_input_weights_file.save'))
        building_output_weights = joblib.load(os.path.join(path,'building_output_weights_file.save'))
        
        # Load models
        building_encoder_model = joblib.load(os.path.join(path,'building_label_encoder_file.save'))
        
        # Prediction
        scores_bld, h_test_bld = elmPredict_optim(SamplesTest, building_input_weights, building_output_weights, 
                                                  config["data_model"]["elm.act_funct"])


        # Floor prediction
        predicted_building = building_encoder_model.inverse_transform(np.argmax(np.transpose(scores_bld), axis=-1))
        
        building = {
            'building_id': str(predicted_building[0])
        }
        return building