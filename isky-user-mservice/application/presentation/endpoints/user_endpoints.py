from pydantic import BaseModel, Field
from . import api_user, user_tag
from application.domain.entity.user_entity import UserEntity
from application.data.model.user_model import UserModel
from application.presentation.data_injection.injection_container import ApplicationContainer
from application.core.decorators.jwt_manager import login_required

# User request body
from application.presentation.req_body.user_body import (UserEmailBody, 
                                                         UserNameBody, 
                                                         UserPasswordBody, 
                                                         UserPhoneBody, 
                                                         UserEmailVerificationBody, 
                                                         UserPhoneVerificationBody, 
                                                         UserStatusBody)

# Use cases
from application.domain.use_cases.get_user_use_case import GetUserUseCase
from application.domain.use_cases.create_user_use_case import CreateUserUseCase
from application.domain.use_cases.delete_user_use_case import DeleteUserUseCase
from application.domain.use_cases.update_user_name_use_case import UpdateUserNameUseCase
from application.domain.use_cases.update_user_email_use_case import UpdateUserEmailUseCase
from application.domain.use_cases.update_user_password_use_case import UpdateUserPasswordUseCase
from application.domain.use_cases.update_user_phone_use_case import UpdateUserPhoneUseCase
from application.domain.use_cases.update_user_email_ver_use_case import UpdateUserEmailVerUseCase
from application.domain.use_cases.update_user_phone_ver_use_case import UpdateUserPhoneVerUseCase
from application.domain.use_cases.update_user_status_use_case import UpdateUserStatusUseCase

class Path(BaseModel):
    user_id: str = Field(..., description='User Id')
    
@api_user.get('/user/<user_id>', tags=[user_tag])
@login_required
def get_user(path: Path):
    get_user_use_case = GetUserUseCase(user_repository=ApplicationContainer.user_repository())
    return get_user_use_case.execute(user_id=path.user_id)

@api_user.post('/user', tags=[user_tag])
@login_required
def create_user(body: UserEntity):
    create_user_use_case = CreateUserUseCase(user_repository=ApplicationContainer.user_repository())
    return create_user_use_case.execute(name=body.name, email=body.email, password=body.password)

@api_user.delete('/user/<user_id>/delete', tags=[user_tag])
@login_required
def delete_user(path:Path):
    delete_user_use_case = DeleteUserUseCase(user_repository=ApplicationContainer.user_repository())
    return delete_user_use_case.execute(user_id=path.user_id)

@api_user.put('/user/<user_id>/update/name', tags=[user_tag])
@login_required
def update_user_name(path:Path, body:UserNameBody):
    update_user_name_use_case = UpdateUserNameUseCase(user_repository=ApplicationContainer.user_repository())
    return update_user_name_use_case.execute(user_id=path.user_id,name=body.name)

@api_user.put('/user/<user_id>/update/email', tags=[user_tag])
@login_required
def update_user_email(path:Path, body:UserEmailBody):
    update_user_email_use_case = UpdateUserEmailUseCase(user_repository=ApplicationContainer.user_repository())
    return update_user_email_use_case.execute(user_id=path.user_id,email=body.email)

@api_user.put('/user/<user_id>/update/password', tags=[user_tag])
@login_required
def update_user_password(path:Path, body:UserPasswordBody):
    update_user_password_use_case = UpdateUserPasswordUseCase(user_repository=ApplicationContainer.user_repository())
    return update_user_password_use_case.execute(user_id=path.user_id,password=body.password)

@api_user.put('/user/<user_id>/update/phone', tags=[user_tag])
@login_required
def update_user_phone(path:Path, body:UserPhoneBody):
    update_user_phone_use_case = UpdateUserPhoneUseCase(user_repository=ApplicationContainer.user_repository())
    return update_user_phone_use_case.execute(user_id=path.user_id,phone=body.phone)

@api_user.put('/user/<user_id>/update/phone_verification', tags=[user_tag])
@login_required
def update_user_phone_ver(path:Path, body:UserPhoneVerificationBody):
    update_user_phone_ver_use_case = UpdateUserPhoneVerUseCase(user_repository=ApplicationContainer.user_repository())
    return update_user_phone_ver_use_case.execute(user_id=path.user_id,verify=body.verify)


@api_user.put('/user/<user_id>/update/email_verification', tags=[user_tag])
@login_required
def update_user_email_ver(path:Path, body:UserEmailVerificationBody):
    update_user_email_ver_use_case = UpdateUserEmailVerUseCase(user_repository=ApplicationContainer.user_repository())
    return update_user_email_ver_use_case.execute(user_id=path.user_id,verify=body.verify)


@api_user.put('/user/<user_id>/update/status', tags=[user_tag])
@login_required
def update_user_status(path:Path, body:UserStatusBody):
    update_user_status_use_case = UpdateUserStatusUseCase(user_repository=ApplicationContainer.user_repository())
    return update_user_status_use_case.execute(user_id=path.user_id,status=body.status)

