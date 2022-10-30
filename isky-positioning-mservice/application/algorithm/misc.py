import json
from colorama import init, Fore, Back, Style
from keras.backend import elu, relu, abs, tanh, sigmoid, sin, cos
from tensorflow.keras.optimizers import Adam, Adamax, Adadelta, Adagrad, Ftrl, Nadam, RMSprop, SGD
import keras.backend as K

class Misc:
    def json_to_dict(self, config_file):
        # Opening JSON file
        with open(config_file) as json_file:
            dictionary = json.load(json_file)
        return dictionary

    def check_key(self, dict, list_parameters):
        for param in range(0, len(list_parameters)):
            if list_parameters[param] in dict.keys():
                pass
            else:
                print(self.log_msg("ERROR", " The following parameter is not found in the configuration file: " +
                                   list_parameters[param]))
                exit(-1)
        return True

    def log_msg(self, level, message):
        init(autoreset=True)
        if level == 'WARNING':
            return Fore.YELLOW + message
        elif level == 'ERROR':
            return Fore.RED + message
        elif level == 'INFO':
            return Style.RESET_ALL + message
        

    def activation_function(self, x, function):
        if function == "tansig":
            r = 2 / (1 + K.exp(-2 * x)) - 1
        elif function == "tanh":
            r = tanh(x)
        elif function == "linsat":
            r = K.abs(1 + x) - K.abs(1 - x)
        elif function == "relu":
            r = relu(x)
        elif function == "elu":
            r = elu(x)
        elif function == "sigmoid":
            r = sigmoid(x)
        elif function == "abs":
            r = abs(x)
        elif function == "sine":
            r = sin(x)
        elif function == "cosine":
            r = cos(x)
        elif function == "linear":
            r = x
        else:
            print(self.log_msg("ERROR", " Activation function not valid."))
            exit(-1)
        return r

    def optimizer(self, opt, lr):
        if opt == 'Adam':
            return Adam(lr)
        elif opt == 'Adamax':
            return Adamax(lr)
        elif opt == 'Adadelta':
            return Adadelta(lr)
        elif opt == 'Adagrad':
            return Adagrad(lr)
        elif opt == 'Ftrl':
            return Ftrl(lr)
        elif opt == 'Nadam':
            return Nadam(lr)
        elif opt == 'RMSprop':
            return RMSprop(lr)
        elif opt == 'SGD':
            return SGD(lr)
        else:
            return Adam(lr)
