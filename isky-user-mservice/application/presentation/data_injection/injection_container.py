import os
from appwrite.client import Client
from dependency_injector import containers, providers
from application.data.datasource.user_datasource_impl import UserDatasourceImpl
from application.data.repository_impl.user_repository_impl import UserRepositoryImpl

from dotenv import load_dotenv

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)

class ApplicationContainer(containers.DeclarativeContainer):
    client = Client()
    
    (
        client
        .set_endpoint(os.environ['APPWRITEENDPOINT'])
        .set_project(os.environ['APPWRITEPROJECTID'])
        .set_key(os.environ['APPWRITEAPIKEY'])
    )

    user_datasource = providers.Factory(UserDatasourceImpl, client)
    user_repository = providers.Factory(UserRepositoryImpl, user_datasource=user_datasource())
    

