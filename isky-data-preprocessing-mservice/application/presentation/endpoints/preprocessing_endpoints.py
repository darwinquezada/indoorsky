import os
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from flask import g, abort

from . import preprocessing_tag, api_preprocessing
# from application.core.decorators.jwt_manager import login_required
from application.domain.entity.preprocessing_entity import PreprocessingEntity
from application.presentation.data_injection.injection_container import ApplicationContainer

# Environment request body
from application.presentation.req_body.preprocessing_body import (PreprocessingIdBody, PreprocessingEnvIdBody)
# Use cases
from application.domain.use_cases.preprocess_data_use_case import PreprocessDataUseCase
from application.domain.use_cases.get_preprocessed_data_by_id_use_case import GetPreprocessedDataByIdUseCase
from application.domain.use_cases.delete_preprocessed_data_by_id_use_case import DeletePreprocessedDataByIdUseCase
from application.domain.use_cases.get_data_preprocessed_by_env_use_case import GetPreprocessedDataByEnvUseCase

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)

r = RethinkDB()

@api_preprocessing.before_request
def before_request():
    try:
        g.rdb_conn = r.connect(host=os.environ['RDB_HOST'], 
                           port=os.environ['RDB_PORT'])
    except RqlDriverError:
        abort(503, "No database g.rdb_connection could be established.")

@api_preprocessing.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.closse()
    except AttributeError:
        pass

@api_preprocessing.post('/preprocess', tags=[preprocessing_tag])
# @login_required
def preprocess_data(body: PreprocessingEntity):
        ipreprocess_data_case = PreprocessDataUseCase(preprocessing_repository=ApplicationContainer.preprocessing_repository())
        data = {
                'name': body.name,
                'env_id': body.env_id,
                'building_id': body.building_id,
                'floor_id': body.floor_id,
                'data_representation': body.data_representation,
                'x_normalization' : body.x_normalization,
                'y_normalization' : body.y_normalization,
                'pos_tech_id': body.pos_tech_id,
                'date_start': body.date_start,
                'date_end': body.date_end,
                'non_dected_value': body.non_dected_value,
                'is_active': body.is_active
                }
        return ipreprocess_data_case.execute(data)

@api_preprocessing.get('/preprocess/<preprocessing_id>', tags=[preprocessing_tag])
# @login_required
def get_preprocessed_data_by_id(path: PreprocessingIdBody):
        get_preprocessed_data_by_id_use_case = GetPreprocessedDataByIdUseCase(preprocessing_repository=ApplicationContainer.preprocessing_repository())
        return get_preprocessed_data_by_id_use_case.execute(conf_prepro_id=path.preprocessing_id)

@api_preprocessing.get('/preprocess/<env_id>/environment', tags=[preprocessing_tag])
# @login_required
def get_preprocessed_data_by_env(path: PreprocessingEnvIdBody):
        get_preprocessed_data_by_env_use_case = GetPreprocessedDataByEnvUseCase(preprocessing_repository=ApplicationContainer.preprocessing_repository())
        return get_preprocessed_data_by_env_use_case.execute(env_id=path.env_id)

@api_preprocessing.delete('/preprocess/<preprocessing_id>/delete', tags=[preprocessing_tag])
# @login_required
def delete_preprocessed_data_by_id(path: PreprocessingIdBody):
        delete_preprocess_data_by_id_use_case = DeletePreprocessedDataByIdUseCase(preprocessing_repository=ApplicationContainer.preprocessing_repository())
        return delete_preprocess_data_by_id_use_case.execute(conf_prepro_id=path.preprocessing_id)

