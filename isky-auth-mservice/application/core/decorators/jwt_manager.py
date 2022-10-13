from http import client
import os
from dotenv import load_dotenv
from functools import wraps
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_current_user
from application.core.exceptions.exceptions import AuthException, InvalidTokenException, UserNotExistException, ExpiredTokenException, TokenNotProvidedException

jwt_manager = JWTManager()

permissions = []

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)

def role_required(name, module, uuid):
    def decorator(func):
        global permissions
        permissions.append([name, module, uuid])
        setattr(func, 'uuid', uuid)

        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user = get_current_user()

            print(user)

        return wrapper

    return decorator


@jwt_manager.user_lookup_loader
def user_lookup_loader_callback(_, jwt_payload):
    user = jwt_payload
    # user = db.session.query(User).filter_by(id=jwt_payload['id']).first()
    if user is None:
        return UserNotExistException()
    return user


@jwt_manager.expired_token_loader
def expired_token_callback(jwt_headers, jwt_payload):
    """token Expired"""
    print(jwt_headers and jwt_payload)
    return ExpiredTokenException()


@jwt_manager.invalid_token_loader
def invalid_token_callback(e):
    """Invalid token"""
    print(e)
    return InvalidTokenException()


@jwt_manager.unauthorized_loader
def unauthorized_callback(e):
    print(e)
    return AuthException()


@jwt_manager.additional_claims_loader
def add_claims_to_access_token(identity):
    return identity
