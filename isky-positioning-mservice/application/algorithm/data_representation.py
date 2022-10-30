#!/usr/bin/python
import numpy as np

'''
Developed by Darwin Quezada 
Date: 2021-02-11
Based on: Octave code provided by Joaquín Torres-Sospedra
'''


class DataRepresentation:
    x_train = 0
    x_test = 0
    type = ""
    def_non_det_val = 0
    new_non_det_val = 0

    def __init__(self, x_train=[], type_rep=None, **kwargs):
        self.x_train = x_train
        self.type = type_rep

        for key, value in kwargs.items():
            if key == "def_no_val":
                self.def_non_det_val = value
            if key == "new_no_val":
                self.new_non_det_val = value

    def data_rep(self):

        if self.def_non_det_val is None or self.def_non_det_val == 0:
            print("No defined a default non detected value")
        else:
            self.x_train = self.data_new_null_db()

        if self.type == "positive":
            x_training = self.positive_rep()
        if self.type == "powed":
            x_training = self.powed_rep()
        if self.type == "exponential":
            x_training = self.exponential_rep()

        return x_training

    def positive_rep(self):
        min_value = np.min(np.min(self.x_train))
        x_training = self.x_train - min_value
        return x_training

    def powed_rep(self):
        min_value = np.min(np.min(self.x_train))
        
        norm_value = np.power((min_value * (-1)), np.exp(1))
        x_training = np.power((self.x_train - min_value), np.exp(1)) / norm_value
        return x_training

    def exponential_rep(self):
        min_value = np.min(np.min(self.x_train))
        norm_value = np.exp((min_value * -1) / 24)
        x_training = np.exp((self.x_train - norm_value) / 24) / norm_value
        
        return x_training

    def data_new_null_db(self):
        x_training = self.datarep_new_null(self.x_train, self.def_non_det_val, self.new_non_det_val)
        return x_training

    def datarep_new_null(self, m, old_null, new_null):
        dif_old_null = np.where(m != old_null, 1, 0)
        eq_old_ull = np.where(m == old_null, 1, 0)
        m1 = m * dif_old_null + new_null * eq_old_ull
        return m1
