import json
import requests
import os
from dotenv import load_dotenv
from flask import jsonify, request
from functools import wraps
from flask_jwt_extended import JWTManager
from application.core.exceptions.auth_exceptions import (AuthException, InvalidTokenException, 
                                                         ExpiredTokenException, TokenNotProvidedException, 
                                                         ConnectionException)

jwt_manager = JWTManager()

permissions = []

# Loading environment variables
dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)


def login_required(f):
    """Execute function if request contains valid access token."""

    @wraps(f)
    def decorated(*args, **kwargs):
        header_token = request.headers.get("Authorization")
        
        if header_token is None:
            return TokenNotProvidedException()
        
        token = header_token.split(" ")
       
        if len(token) > 1:
            response = requests.request(method="GET", url=os.environ['AUTHENDPOINT']+token[1], verify=False)
        else:
            response = requests.request(method="GET", url=os.environ['AUTHENDPOINT']+token[0], verify=False)
            
        auth_response = response.json()
        
        if 'code' in auth_response:
            return jsonify({'code': auth_response['code'], 'message': auth_response['message']})
        
        if response.status_code == 404:
            return ConnectionException()
        
        if response.status_code == 401:
            return AuthException()
        
        return f(*args, **kwargs)
    return decorated


@jwt_manager.expired_token_loader
def expired_token_callback(jwt_headers, jwt_payload):
    """token Expired"""
    return ExpiredTokenException()


@jwt_manager.invalid_token_loader
def invalid_token_callback(e):
    """Invalid token"""
    return InvalidTokenException()


@jwt_manager.unauthorized_loader
def unauthorized_callback(e):
    """Unauthorized"""
    return AuthException()


@jwt_manager.additional_claims_loader
def add_claims_to_access_token(identity):
    """Request access token"""
    return identity
