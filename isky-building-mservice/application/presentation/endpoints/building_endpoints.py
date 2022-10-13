import os
from pydoc import cli
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

from pydoc import describe
from . import building_tag, api_building
from application.core.decorators.jwt_manager import login_required
from application.data.model.building_model import BuildingModel
from application.domain.entity.building_entity import BuildingEntity
from application.presentation.data_injection.injection_container import ApplicationContainer
from flask import jsonify, g, abort
# Environment request body
from application.presentation.req_body.building_body import (BuildingIdBody, BuildingNameBody, BuildingBody)
# Use cases
from application.domain.use_cases.insert_building_use_case import InsertBuildingUseCase
from application.domain.use_cases.get_building_by_id_use_case import GetBuildingByIdUseCase
from application.domain.use_cases.get_building_by_name_use_case import GetBuildingByNameUseCase
from application.domain.use_cases.update_building_use_case import UpdateBuildingUseCase
from application.domain.use_cases.delete_building_use_case import DeleteBuildingUseCase

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)

r = RethinkDB()

@api_building.before_request
def before_request():
    try:
        g.rdb_conn = r.connect(host=os.environ['RDB_HOST'], 
                           port=os.environ['RDB_PORT'])
    except RqlDriverError:
        abort(503, "No database g.rdb_connection could be established.")

@api_building.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.closse()
    except AttributeError:
        pass

@api_building.post('/building', tags=[building_tag])
@login_required
def insert_building(body: BuildingBody):
        insert_environment_use_case = InsertBuildingUseCase(building_repository=ApplicationContainer.building_repository())
        data = {
                "env_id": body.env_id,
                "name": body.name,
                "description": body.description,
                "num_floors": body.num_floors,
                "latitude": body.latitude,
                "longitude": body.longitude,
                "altitude": body.altitude,
                "is_active": body.is_active,
                "is_public": body.is_public
                }
        return insert_environment_use_case.execute(data)

@api_building.get('/building/<building_id>', tags=[building_tag])
@login_required
def get_building_by_id(path: BuildingIdBody):
        get_building_by_id_use_case = GetBuildingByIdUseCase(building_repository=ApplicationContainer.building_repository())
        return get_building_by_id_use_case.execute(building_id=path.building_id)

@api_building.get('/building/<name>/name', tags=[building_tag])
@login_required
def get_building_by_name(path: BuildingNameBody):
        get_building_by_name_use_case = GetBuildingByNameUseCase(building_repository=ApplicationContainer.building_repository())
        return get_building_by_name_use_case.execute(name=path.name)

@api_building.delete('/building/<building_id>/delete', tags=[building_tag])
@login_required
def delete_building_by_id(path: BuildingIdBody):
        delete_use_case = DeleteBuildingUseCase(building_repository=ApplicationContainer.building_repository())
        return delete_use_case.execute(building_id=path.building_id)

@api_building.put('/building/<building_id>/update', tags=[building_tag])
@login_required
def update_building(path:BuildingIdBody, body:BuildingBody):
        update_building_use_case = UpdateBuildingUseCase(building_repository=ApplicationContainer.building_repository())
        return update_building_use_case.execute(building_id=path.building_id, env_id=body.env_id, 
                              name=body.name, num_floors=body.num_floors, description=body.description,
                              latitude=body.latitude, longitude=body.longitude, altitude=body.altitude,
                              is_public=body.is_public, is_active=body.is_active)