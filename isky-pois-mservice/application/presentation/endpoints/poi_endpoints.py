import os
from pydoc import cli
from dotenv import load_dotenv
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

from pydoc import describe
from . import poi_tag, api_poi
from application.core.decorators.jwt_manager import login_required
from application.data.model.poi_model import PoiModel
from application.domain.entity.poi_entity import PoiEntity
from application.presentation.data_injection.injection_container import ApplicationContainer
from flask import jsonify,g,abort
# Environment request body
from application.presentation.req_body.poi_body import (PoiNameBody, PoiIdBody)
# Use cases
from application.domain.use_cases.insert_poi_use_case import InsertPoiUseCase
from application.domain.use_cases.get_poi_by_id_use_case import GetPoiByIdUseCase
from application.domain.use_cases.get_poi_by_name_use_case import GetPoiByNameUseCase
from application.domain.use_cases.update_poi_use_case import UpdatePoiUseCase
from application.domain.use_cases.delete_poi_use_case import DeletePoiUseCase

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)

r = RethinkDB()

@api_poi.before_request
def before_request():
    try:
        g.rdb_conn = r.connect(host=os.environ['RDB_HOST'], port=os.environ['RDB_PORT'], 
                               user=os.environ['RDB_USER'],
                               password=os.environ['RDB_PASSWORD'])
    except RqlDriverError:
        abort(503, "No database g.rdb_connection could be established.")

@api_poi.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.closse()
    except AttributeError:
        pass

@api_poi.post('/poi', tags=[poi_tag])
@login_required
def insert_poi(body: PoiEntity):
        insert_environment_use_case = InsertPoiUseCase(poi_repository=ApplicationContainer.poi_repository())
        data = {
                "floor_id": body.floor_id,
                "name": body.name,
                "description": body.description,
                "image": body.image,
                "latitude": body.latitude,
                "longitude": body.longitude,
                "altitude": body.altitude,
                "pos_x": body.pos_x,
                "pos_y": body.pos_y,
                "pos_z": body.pos_z,
                "is_active": body.is_active,
                "is_public": body.is_public
                }
        return insert_environment_use_case.execute(data)

@api_poi.get('/poi/<poi_id>', tags=[poi_tag])
@login_required
def get_poi_by_id(path: PoiIdBody):
        get_poi_by_id_use_case = GetPoiByIdUseCase(poi_repository=ApplicationContainer.poi_repository())
        return get_poi_by_id_use_case.execute(poi_id=path.poi_id)

@api_poi.get('/poi/<name>/name', tags=[poi_tag])
@login_required
def get_poi_by_name(path: PoiNameBody):
        get_poi_by_name_use_case = GetPoiByNameUseCase(poi_repository=ApplicationContainer.poi_repository())
        return get_poi_by_name_use_case.execute(name=path.name)

@api_poi.delete('/poi/<poi_id>/delete', tags=[poi_tag])
@login_required
def delete_poi_by_id(path: PoiIdBody):
        delete_use_case = DeletePoiUseCase(poi_repository=ApplicationContainer.poi_repository())
        return delete_use_case.execute(poi_id=path.poi_id)

@api_poi.put('/poi/<poi_id>/update', tags=[poi_tag])
@login_required
def update_poi(path:PoiIdBody, body:PoiEntity):
        update_poi_use_case = UpdatePoiUseCase(poi_repository=ApplicationContainer.poi_repository())
        return update_poi_use_case.execute(poi_id=path.poi_id, floor_id=body.floor_id, name=body.name, 
                                           description=body.description, image=body.image, latitude=body.latitude, 
                                           longitude=body.longitude, altitude=body.altitude, pos_x=body.pos_x, 
                                           pos_y=body.pos_y, pos_z=body.pos_z, is_active=body.is_active, 
                                           is_public=body.is_public)