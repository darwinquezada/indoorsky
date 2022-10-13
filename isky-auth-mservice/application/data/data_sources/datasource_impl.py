from flask import jsonify
from .datasource import IDataSource
from dependency_injector.wiring import inject
from appwrite.exception import AppwriteException
from appwrite.client import Client
from appwrite.services.account import Account


class DataSourceImpl(IDataSource):
    
    def verify_token(self, endpoint: str, project_id: str, jwt_token: str) -> dict:
        try:
            client = Client()
            (
                client
                .set_endpoint(endpoint)
                .set_project(project_id)
                .set_jwt(jwt_token)
            )
            
            account = Account(client=client)
            result = account.get()
            return result
        except AppwriteException as e:
            return jsonify({'code': e.code, 'message': e.message})