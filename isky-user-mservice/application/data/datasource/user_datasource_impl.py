from pydoc import cli
from urllib import response
from application.data.datasource.user_datasource import IUserDatasource
from appwrite.client import Client
from appwrite.services.users import Users
from appwrite.exception import AppwriteException
from flask import jsonify

class UserDatasourceImpl(IUserDatasource):
    
    def __init__(self, client: Client) -> None:
        self.client = client
        
    def get_user(self, user_id: str) -> dict:
        try:
            user = Users(self.client)
            response = user.get(user_id=user_id)
            return response
        except AppwriteException as e:
            return jsonify({'code': e.code, 'message': e.message})
        
    def create_user(self, name:str, email: str, password: str) -> dict:
        try:
            user = Users(self.client)
            response = user.create(user_id='unique()', name=name, email=email, password=password)
            return response
        except AppwriteException as e:
            return jsonify({'code': e.code, 'message': e.message})
        
    def delete_user(self, user_id: str) -> dict:
        try:
            user = Users(self.client)
            response = user.delete(user_id=user_id)
            return response
        except AppwriteException as e:
            return jsonify({'code': e.code, 'message': e.message})
        
    def update_user_name(self, user_id: str, name: str) -> dict:
        try:
            user = Users(self.client)
            response = user.update_name(user_id=user_id, name=name)
            return response
        except AppwriteException as e:
            return jsonify({'code': e.code, 'message': e.message})
        
    def update_user_email(self, user_id: str, email: str) -> dict:
        try:
            user = Users(self.client)
            response = user.update_email(user_id=user_id, email=email)
            return response
        except AppwriteException as e:
            return jsonify({'code': e.code, 'message': e.message})
        
    def update_user_password(self, user_id: str, password: str) -> dict:
        try:
            user = Users(self.client)
            response = user.update_password(user_id=user_id, password=password)
            return response
        except AppwriteException as e:
            return jsonify({'code': e.code, 'message': e.message})
        
    def update_user_phone(self, user_id: str, phone: str) -> dict:
        try:
            user = Users(self.client)
            response = user.update_phone(user_id=user_id, number=phone)
            return response
        except AppwriteException as e:
            return jsonify({'code': e.code, 'message': e.message})
    
    def update_user_email_verification(self, user_id: str, verify: bool) -> dict:
        try:
            user = Users(self.client)
            response = user.update_email_verification(user_id=user_id, email_verification=verify)
            return response
        except AppwriteException as e:
            return jsonify({'code': e.code, 'message': e.message})
    
    def update_user_phone_verification(self, user_id: str, verify: bool) -> dict:
        try:
            user = Users(self.client)
            response = user.update_phone_verification(user_id=user_id, phone_verification=verify)
            return response
        except AppwriteException as e:
            return jsonify({'code': e.code, 'message': e.message})
    
    def update_user_status(self, user_id: str, status: bool) -> dict:
        try:
            user = Users(self.client)
            response = user.update_status(user_id=user_id, status=status)
            return response
        except AppwriteException as e:
            return jsonify({'code': e.code, 'message': e.message})