from email import message
import os
from appwrite.client import Client
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from dependency_injector import containers, providers
from application.data.repository_impl.preprocessing_repository_impl import PreprocessingRepositoryImpl
from application.data.datasource.preprocessing_datasource_impl import PreprocessingDatasourceImpl
from dotenv import load_dotenv
from flask import jsonify, abort

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
        
    preprocessing_datasource = providers.Factory(PreprocessingDatasourceImpl,
                                                client=client,
                                                database_name=os.environ['RDB_DB'],
                                                table_config=os.environ['TABLE_PREPROCESSING'],
                                                table_data=os.environ['TABLE_FILE'],
                                                table_dataset=os.environ['TABLE_DATASET']
                                                )
    
    preprocessing_repository = providers.Factory(PreprocessingRepositoryImpl,
                                         preprocessing_datasource=preprocessing_datasource())
