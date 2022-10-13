from . import api_model, model_tag
from application.domain.entity.cnn_elm_entity import CnnElmEntity
from application.domain.entity.cnn_lstm_entity import CnnLstmEntity

from application.presentation.data_injection.injection_container import ApplicationContainer
from application.core.decorators.jwt_manager import login_required

# User request body
from application.presentation.req_body.model_body import (ModelIdBody, ModelNameBody, FloorBody)

# Use cases
from application.domain.use_cases.train_model_use_case import TrainModelUseCase
from application.domain.use_cases.get_model_by_id_use_case import GetModelByIdUseCase
from application.domain.use_cases.get_model_by_name_use_case import GetModelByNameUseCase
from application.domain.use_cases.delete_model_by_id_use_case import DeleteModelByIdUseCase


@api_model.post('/model/train/cnn_lstm', tags=[model_tag])
#@login_required
def training_model_cnn_lstm(body:CnnLstmEntity):
    floor = {
        'lr':  body.floor.lr,
        'epochs': body.floor.epochs,
        'batch_size': body.floor.batch_size,
        'loss': body.floor.loss,
        'optimizer': body.floor.optimizer 
        }
    building = {
        'lr':  body.building.lr,
        'epochs': body.building.epochs,
        'batch_size': body.building.batch_size,
        'loss': body.building.loss,
        'optimizer': body.building.optimizer 
        }
    position = {
        'lr':  body.position.lr,
        'epochs': body.position.epochs,
        'batch_size': body.position.batch_size,
        'loss': body.position.loss,
        'optimizer': body.position.optimizer 
        }
    
    test = {
        'percent_test' : body.test.percent_test,
        'test_accuracy' : body.test.test_accuracy,
    }
    
    data = {
        'name': body.name,
        'dataset_id': body.dataset_id,
        'floor': floor,
        'building': building,
        'position': position,
        'test': test,
        'is_active': body.is_active
    }
    training_model_use_case = TrainModelUseCase(model_repository=ApplicationContainer.model_repository())
    return training_model_use_case.execute(data=data, model='cnn_lstm')

@api_model.post('/model/train/cnn_elm', tags=[model_tag])
#@login_required
def training_model_cnn_elm(body: CnnElmEntity):
    cnn = {
        'padding': body.cnn.padding.value,
        'strides': body.cnn.strides,
        'data_format': body.cnn.data_format.value,
        'act_funct': body.cnn.act_funct.value,
        'kernel_size': body.cnn.kernel_size,
        'filter': body.cnn.filter
    }
    elm = {
        'act_funct': body.elm.act_funct.value,
        'c': body.elm.c,
        'hidden_neurons': body.elm.hidden_neurons,
        'weight_intialization': body.elm.weight_intialization.value,
        'weight_initializatio_bits': body.elm.weight_initializatio_bits,
        'output_weits_bits': body.elm.output_weits_bits
    }
    
    test = {
        'percent_test' : body.test.percent_test,
        'test_accuracy' : body.test.test_accuracy,
        'k' : body.test.k,
        'distance_metric': body.test.distance_metric.value
    }
    
    data = {
        'name': body.name,
        'dataset_id': body.dataset_id,
        'cnn': cnn,
        'elm': elm,
        'test': test,
        'is_active': body.is_active
    }
    
    training_model_use_case = TrainModelUseCase(model_repository=ApplicationContainer.model_repository())
    return training_model_use_case.execute(data=data, model='cnn_elm')