from pydantic import BaseModel, Field
from . import api_cleansing, cleansing_tag
from application.domain.entity.cleansing_entity import CleansingEntity

from application.presentation.data_injection.injection_container import ApplicationContainer
from application.core.decorators.jwt_manager import login_required

# User request body
from application.presentation.req_body.cleansing_body import (CleansingEnvIdBody, 
                                                              CleansingIdBody,
                                                              CleansingNameBody)

# Use cases
from application.domain.use_cases.cleansing_dataset_use_case import DataCleansingUseCase
from application.domain.use_cases.get_cleansed_dataset_by_env_use_case import GetCleansedDatasetByEnvIdUseCase
from application.domain.use_cases.get_cleansed_dataset_by_id_use_case import GetCleansedDatasetByIdUseCase
from application.domain.use_cases.get_cleansed_dataset_by_name_use_case import GetCleansedDatasetByNameUseCase
from application.domain.use_cases.delete_cleansed_dataset_use_case import DeleteCleansedDatasetUseCase

@api_cleansing.post('/cleansing/clean_dataset', tags=[cleansing_tag])
@login_required
def data_cleansing(body: CleansingEntity):
    test_data = {
        "percent_test": body.test.percent_test,
        "test_accuracy": body.test.test_accuracy,
        "k": body.test.k,
        "distance_metric": body.test.distance_metric
    }
    data = {
        'name': body.name,
        'threshold': body.threshold,
        'dataset_id': body.dataset_id,
        'test': test_data
    }
    data_cleansing_use_case = DataCleansingUseCase(cleansing_repository=ApplicationContainer.cleansing_repository())
    return data_cleansing_use_case.execute(data=data)

@api_cleansing.get('/cleansing/<cleansing_id>', tags=[cleansing_tag])
@login_required
def get_data_cleansed_by_id(path: CleansingIdBody):
    get_data_cleansed_by_id_use_case = GetCleansedDatasetByIdUseCase(cleansing_repository=ApplicationContainer.cleansing_repository())
    return get_data_cleansed_by_id_use_case.execute(clean_id=path.cleansing_id)

@api_cleansing.get('/cleansing/<name>/name', tags=[cleansing_tag])
@login_required
def get_data_cleansed_by_name(path: CleansingNameBody):
    get_data_cleansed_by_name_use_case = GetCleansedDatasetByNameUseCase(cleansing_repository=ApplicationContainer.cleansing_repository())
    return get_data_cleansed_by_name_use_case.execute(name=path.name)

@api_cleansing.get('/cleansing/<env_id>/environment', tags=[cleansing_tag])
@login_required
def get_data_cleansed_by_env_id(path: CleansingEnvIdBody):
    get_data_cleansed_by_env_id_use_case = GetCleansedDatasetByEnvIdUseCase(cleansing_repository=ApplicationContainer.cleansing_repository())
    return get_data_cleansed_by_env_id_use_case.execute(env_id=path.env_id)

@api_cleansing.delete('/cleansing/<cleansing_id>/delete', tags=[cleansing_tag])
@login_required
def delete_data_cleansed_by_id(path: CleansingIdBody):
    delete_data_cleansed_by_id_use_case = DeleteCleansedDatasetUseCase(cleansing_repository=ApplicationContainer.cleansing_repository())
    return delete_data_cleansed_by_id_use_case.execute(clean_id=path.cleansing_id)
