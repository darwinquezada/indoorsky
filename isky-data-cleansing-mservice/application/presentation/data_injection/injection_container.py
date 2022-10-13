import os
from appwrite.client import Client
from dependency_injector import containers, providers
from application.data.datasource.cleansing_datasource_impl import DataCleansingDatasourceImpl
from application.data.repository_impl.cleansing_repository_impl import DataCleansingRepositoryImpl

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
    
    tables = {
        'preprocessing': os.environ['TABLE_PREPROCESSING'],
        'file_preprocessing': os.environ['TABLE_FILE'],
        'dataset': os.environ['TABLE_DATASET'],
        'cleansing': os.environ['TABLE_CLEANSING']
    }

    cleansing_datasource = providers.Factory(DataCleansingDatasourceImpl, client=client, 
                                             database_name=os.environ['RDB_DB'], tables=tables)
    cleansing_repository = providers.Factory(DataCleansingRepositoryImpl, cleansing_datasource=cleansing_datasource())
    

