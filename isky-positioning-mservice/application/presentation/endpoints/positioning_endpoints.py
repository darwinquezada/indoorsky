from statistics import mode
from application.domain.use_cases.get_position_use_case import GetPositionUseCase
from application.domain.use_cases.set_mode_use_case import SetPositionModelUseCase
from application.domain.use_cases.delete_set_model_use_case import DeleteSetModelUseCase
from application.domain.use_cases.update_set_model_use_case import UpdateSetModelUseCase
from application.domain.use_cases.get_set_model_by_model_type_use_case import GetSetModelByModelTypeUseCase
from . import positioning_tag, api_positioning
from application.core.decorators.jwt_manager import login_required
from application.presentation.data_injection.injection_container import ApplicationContainer
from application.presentation.req_body.position_body import (ModelIdBody, ListWifiBody, 
                                                             ListBleBody, ModelBody, ModelTypeBody,
                                                             PathGetPostionBody)


@api_positioning.post('/positioning/pos_tech/<pos_tech_id>/model_type/<model_type>', tags=[positioning_tag])
# @login_required
def get_position_wifi(path:PathGetPostionBody, body: ListWifiBody ):
        get_position_use_case = GetPositionUseCase(positioning_repository=ApplicationContainer.positioning_repository())
        return get_position_use_case.execute(pos_tech_id=path.pos_tech_id, model_type=path.model_type.value, data=body.list_wifi)

@api_positioning.post('/positioning/ble', tags=[positioning_tag])
# @login_required
def get_position_ble( body: ListBleBody ):
        get_position_use_case = GetPositionUseCase(positioning_repository=ApplicationContainer.positioning_repository())
        return get_position_use_case.execute(data=body.list_ble)

@api_positioning.post('/positioning/set_model', tags=[positioning_tag])
# @login_required
def set_position_model( body: ModelBody ):
        data = {
                'data_model_id': body.data_model_id,
                'model': body.model.value,
                'model_type': body.model_type.value,
                'pos_tech_id': body.pos_tech_id
        }
        set_position_model_use_case = SetPositionModelUseCase(positioning_repository=ApplicationContainer.positioning_repository())
        return set_position_model_use_case.execute(model=data)

@api_positioning.get('/positioning/set_model/<model_type>', tags=[positioning_tag])
# @login_required
def get_set_model_by_model_type( path:ModelTypeBody):
        
        get_set_model_by_model_type_use_case = GetSetModelByModelTypeUseCase(positioning_repository=ApplicationContainer.positioning_repository())
        return get_set_model_by_model_type_use_case.execute(model_type=path.model_type.value)

@api_positioning.delete('/positioning/set_model/<model_id>/delete', tags=[positioning_tag])
# @login_required
def delete_set_position_model( path:ModelIdBody):
        delete_set_position_model_use_case = DeleteSetModelUseCase(positioning_repository=ApplicationContainer.positioning_repository())
        return delete_set_position_model_use_case.execute(set_model_id=path.model_id)

# @api_positioning.put('/position/set_model/<model_id>/update', tags=[positioning_tag])
# @login_required
# def update_set_position_model(path:ModelIdBody, body:ModelBody):
#         data = {
#                 'data_model_id': body.data_model_id,
#                 'model': body.model.value,
#                 'model_type': body.model_type.value,
#                 'pos_tech_id': body.pos_tech_id
#         }
#         update_set_position_model_use_case = UpdateSetModelUseCase(positioning_repository=ApplicationContainer.positioning_repository())
#         return update_set_position_model_use_case.execute(set_model_id=path.model_id, model=data)