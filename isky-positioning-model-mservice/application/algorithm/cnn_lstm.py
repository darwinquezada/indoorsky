from pyexpat import model
import pandas as pd
from numpy import array
import tensorflow as tf
import os
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, LabelEncoder
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Flatten, Dropout, TimeDistributed, Bidirectional
from tensorflow.keras.layers import Conv1D, MaxPooling1D
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras import regularizers
from numpy.random import seed, default_rng
import numpy as np
from misc import Misc
import joblib

from data_preprocessing import data_reshape_stf

import matplotlib.pyplot as plt

### Warning ###
import warnings
warnings.filterwarnings('ignore')

# For reproducibility
rnd_seed = 1102
default_rng(rnd_seed)
tf.random.set_seed(
    rnd_seed
)

gpu_available = tf.test.is_gpu_available()

if gpu_available:
    device_name = tf.test.gpu_device_name()
    if device_name != '/device:GPU:0':
        raise SystemError('GPU device not found')
    print('Found GPU at: {}'.format(device_name))


class CNN_LSTM():
    def __init__(self, X_data, y_data,
                building_config, floor_config, position_config,):
        
        self.X_data = X_data
        self.y_data = y_data
        self.building_config = building_config
        self.floor_config = floor_config
        self.position_config = position_config
        self.classes_floor = np.shape(self.y_data['y_train']['floor'])[1]
        self.classes_bld = np.shape(self.y_data['y_train']['building'])[1]
        self.gan_general_conf = None
        self.data_augmentation = None
        self.method = None

    # Model to classify the fingerprints into buildings
    def building_model(self):
        X_train, X_test, X_valid = data_reshape_stf(self.X_data['X_train'], self.X_data['X_test'], 
                                                    self.X_data['X_validation'])
        self.bl_model = Sequential()
        self.bl_model.add(TimeDistributed(Conv1D(filters=16, kernel_size=1, activation='relu'),
                                          input_shape=(None, X_train.shape[2], X_train.shape[3]))) 
        self.bl_model.add(TimeDistributed(MaxPooling1D(pool_size=2))) # 
        self.bl_model.add(TimeDistributed(Dropout(0.8))) 
        self.bl_model.add(TimeDistributed(Flatten()))
        self.bl_model.add(LSTM(40, activation='relu')) 
        self.bl_model.add(Dense(self.classes_bld, activation='softmax'))

    # Model to classify the fingerprints into floor
    def floor_model(self):
        X_train, X_test, X_valid = data_reshape_stf(self.X_data['X_train'], self.X_data['X_test'], 
                                                    self.X_data['X_validation'])
        self.fl_model = Sequential()
        self.fl_model.add(TimeDistributed(Conv1D(filters=16, kernel_size=1, activation='relu'),
                                          input_shape=(None, X_train.shape[2], X_train.shape[3]))) 
        self.fl_model.add(TimeDistributed(MaxPooling1D(pool_size=2)))  # 1
        self.fl_model.add(TimeDistributed(Dropout(0.5)))
        self.fl_model.add(TimeDistributed(Conv1D(filters=32, kernel_size=1, activation='relu',
                                                 padding='same')))
        self.fl_model.add(TimeDistributed(MaxPooling1D(pool_size=1)))
        self.fl_model.add(TimeDistributed(Dropout(0.5)))
        self.fl_model.add(TimeDistributed(Flatten()))
        self.fl_model.add(LSTM(50, activation='relu'))
        self.fl_model.add(Dense(self.classes_floor, activation='softmax'))

    # Regression model to predict the position (x,y,z)
    def position_model(self):
        X_train, X_test, X_valid = data_reshape_stf(self.X_data['X_train'], self.X_data['X_test'], 
                                                    self.X_data['X_validation'])
        self.pos_model = Sequential()
        self.pos_model.add(TimeDistributed(Conv1D(filters=8, kernel_size=1, activation='elu'),
                                           input_shape=(None, X_train.shape[2], X_train.shape[3])))
        self.pos_model.add(TimeDistributed(MaxPooling1D(pool_size=1)))
        self.pos_model.add(TimeDistributed(Dropout(0.5)))
        self.pos_model.add(TimeDistributed(Conv1D(filters=8, kernel_size=1, activation='elu', padding='same')))
        self.pos_model.add(TimeDistributed(MaxPooling1D(pool_size=1)))
        self.pos_model.add(TimeDistributed(Dropout(0.5)))
        self.pos_model.add(TimeDistributed(Flatten()))
        self.pos_model.add(LSTM(40, activation='elu'))
        self.pos_model.add(Dense(3, activation='elu'))

    def train(self):
        X_train, X_test, X_valid = data_reshape_stf(self.X_data['X_train'], self.X_data['X_test'], 
                                                    self.X_data['X_validation'])

        if np.size(X_valid) == 0:
            monitor = 'loss'
        else:
            monitor = 'val_loss'

        # EarlyStopping
        early_stopping = EarlyStopping(monitor=monitor,
                                       min_delta=0,
                                       patience=5,
                                       verbose=1,
                                       mode='auto')  # val_loss

        misc = Misc()

        # ---------------------------------------- Building ------------------------------------------
        if self.building_config['train'] == True:
            print("WARNING", "--------- BUILDING CLASSIFICATION -----------")

            self.building_model()
            optimizer = misc.optimizer(self.building_config['optimizer'], self.building_config['lr'])
            self.bl_model.compile(loss=self.building_config['loss'], optimizer=optimizer) 

            if np.size(X_valid) == 0:
                bld_history = self.bl_model.fit(X_train, self.y_data['y_train']['building'], 
                                                epochs=self.building_config['epochs'], verbose=1,
                                                callbacks=[early_stopping])
            else:
                bld_history = self.bl_model.fit(X_train, self.y_data['y_train']['building'], 
                                                validation_data=(X_valid, self.y_data['y_validation']['building']),
                                                epochs=self.building_config['epochs'], verbose=1,
                                                callbacks=[early_stopping])

        # ---------------------------------------- Floor --------------------------------------------
        if self.floor_config['train'] == True:
            print(misc.log_msg("WARNING", "--------- FLOOR CLASSIFICATION -----------"))

            self.floor_model()
            optimizer = misc.optimizer(self.floor_config['optimizer'], self.floor_config['lr'])
            self.fl_model.compile(loss=self.floor_config['loss'], optimizer=optimizer) #, metrics=['accuracy'])

            if np.size(X_valid) == 0:
                floor_history = self.fl_model.fit(X_train, self.y_data['y_train']['floor'], epochs=self.floor_config['epochs'], verbose=1,
                                                  callbacks=[early_stopping])
            else:
                floor_history = self.fl_model.fit(X_train, self.y_data['y_train']['floor'], 
                                                  validation_data=(X_valid, self.y_data['y_validation']['floor']),
                                                  epochs=self.floor_config['epochs'], verbose=1,
                                                  callbacks=[early_stopping])

        # --------------------------- Position (Latitude, Longitude and altitude) ----------------------
        if self.position_config['train'] == True:
            print(misc.log_msg("WARNING", "------- LONGITUDE, LATITUDE and ALTITUDE PREDICTION -------"))

            self.position_model()
            optimizer = misc.optimizer(self.position_config['optimizer'],
                                       self.position_config['lr'])
            self.pos_model.compile(loss=self.position_config['loss'], optimizer=optimizer)

            train_data = np.hstack([self.y_data['y_train']['position']['LONGITUDE'].values.reshape(-1, 1),
                                    self.y_data['y_train']['position']['LATITUDE'].values.reshape(-1, 1),
                                    self.y_data['y_train']['position']['ALTITUDE'].values.reshape(-1, 1)])

            if np.size(X_valid) == 0:
                pos_history = self.pos_model.fit(X_train, train_data, epochs=self.position_config['epochs'],
                                                 verbose=1, callbacks=[early_stopping])

            else:
                valid_data = np.hstack([self.y_data['y_validation']['position']['LONGITUDE'].values.reshape(-1, 1),
                                    self.y_data['y_validation']['position']['LATITUDE'].values.reshape(-1, 1),
                                    self.y_data['y_validation']['position']['ALTITUDE'].values.reshape(-1, 1)])
                pos_history = self.pos_model.fit(X_train, train_data,
                                                 validation_data=(X_valid, valid_data),
                                                 epochs=self.position_config['epochs'],
                                                 verbose=1, callbacks=[early_stopping])

        return self.pos_model, self.fl_model, self.bl_model
