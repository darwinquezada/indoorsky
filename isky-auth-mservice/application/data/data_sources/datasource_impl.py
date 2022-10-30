from flask import jsonify
from .datasource import IDataSource
from dependency_injector.wiring import inject
from appwrite.exception import AppwriteException
from appwrite.client import Client
from appwrite.services.account import Account
from application.core.exceptions.status_codes import InternalServerErrorResponseCode


class DataSourceImpl(IDataSource):
    
    def verify_token(self, endpoint: str, project_id: str, jwt_token: str) -> dict:
        """
        Verify token
        Parameters:
        endpoint: URL, 
        project_id: Appwrite project ID, 
        jwt_token: Appwrite JWT token
        Return:
        User information (Dictionary)
        """
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
            return InternalServerErrorResponseCode(message=e.message)