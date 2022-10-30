import os
from pydoc import cli
from turtle import pos
from dotenv import load_dotenv
from application.core.decorators.jwt_manager import login_required
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from flask import g, abort

from . import api_pos_tech, pos_tech_tag

from application.presentation.req_body.pos_tech_body import (PosTechIdBody, PosTechNameBody)

from application.domain.entity.pos_tech_entity import PosTechEntity
from application.domain.use_cases.delete_pos_tech_by_id_use_case import DeletePosTechByIdPosTechUseCase
from application.domain.use_cases.get_pos_tech_by_id_use_case import GetPosTechByIdPosTechUseCase
from application.domain.use_cases.get_pos_tech_by_name_use_case import GetPosTechByNamePosTechUseCase
from application.domain.use_cases.insert_pos_tech_use_case import InsertPosTechUseCase
from application.domain.use_cases.update_pos_tech_by_id_use_case import UpdatePosTechByIdPosTechUseCase

from application.presentation.data_injection.injection_container import ApplicationContainer

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)

r = RethinkDB()

@api_pos_tech.before_request
def before_request():
    try:
        g.rdb_conn = r.connect(host=os.environ['RDB_HOST'], port=os.environ['RDB_PORT'], 
                               user=os.environ['RDB_USER'],
                               password=os.environ['RDB_PASSWORD'])
    except RqlDriverError:
        abort(503, "No database connection could be established.")

@api_pos_tech.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.closse()
    except AttributeError:
        pass
    
@api_pos_tech.post('/pos_tech', tags=[pos_tech_tag])
@login_required
def insert_pos_tech(body: PosTechEntity):
        insert_pos_tech_use_case = InsertPosTechUseCase(pos_tech_repository=ApplicationContainer.pos_tech_repository())
        data = {
                "name": body.name,
                "code": body.code,
                "is_active": body.is_active
                }
        return insert_pos_tech_use_case.execute(data)
    
@api_pos_tech.get('/pos_tech/<pos_tech_id>', tags=[pos_tech_tag])
@login_required
def get_pos_tech_by_id(path: PosTechIdBody):
        get_pos_tech_by_id_use_case = GetPosTechByIdPosTechUseCase(pos_tech_repository=ApplicationContainer.pos_tech_repository())
        return get_pos_tech_by_id_use_case.execute(pos_tech_id=path.pos_tech_id)

@api_pos_tech.get('/pos_tech/<name>/name', tags=[pos_tech_tag])
@login_required
def get_pos_tech_by_name(path: PosTechNameBody):
        get_pos_tech_by_name_use_case = GetPosTechByNamePosTechUseCase(pos_tech_repository=ApplicationContainer.pos_tech_repository())
        return get_pos_tech_by_name_use_case.execute(name=path.name)
    
@api_pos_tech.delete('/pos_tech/<pos_tech_id>/delete', tags=[pos_tech_tag])
@login_required
def delete_pos_tech_by_id(path: PosTechIdBody):
        delete_pos_tech_by_id_use_case = DeletePosTechByIdPosTechUseCase(pos_tech_repository=ApplicationContainer.pos_tech_repository())
        return delete_pos_tech_by_id_use_case.execute(pos_tech_id=path.pos_tech_id)
    
@api_pos_tech.put('/pos_tech/<pos_tech_id>/update', tags=[pos_tech_tag])
@login_required
def update_pos_tech(path:PosTechIdBody, body:PosTechEntity):
        data = {
                "name": body.name,
                "code": body.code,
                "is_active": body.is_active
                }
        update_pos_tech_use_case = UpdatePosTechByIdPosTechUseCase(pos_tech_repository=ApplicationContainer.pos_tech_repository())
        return update_pos_tech_use_case.execute(pos_tech_id=path.pos_tech_id, data=data)