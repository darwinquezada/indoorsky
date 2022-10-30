import os
from appwrite.client import Client
from dependency_injector import containers, providers
from application.data.data_source.positioning_datasource_impl import PositioningDatasourceImpl
from application.data.repository_impl.positioning_repository_impl import PositioningRepositoryImpl

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
        'file_preprocessing': os.environ['TABLE_FILE_PREPROCESSING'],
        'file_model': os.environ['TABLE_FILE'],
        'dataset': os.environ['TABLE_DATASET'],
        'data_model': os.environ['TABLE_DATA_MODEL'],
        'model': os.environ['TABLE_MODEL']
    }

    positioning_datasource = providers.Factory(PositioningDatasourceImpl, client=client, 
                                             database_name=os.environ['RDB_DB'], tables=tables)
    positioning_repository = providers.Factory(PositioningRepositoryImpl, positioning_datasource=positioning_datasource())
    


