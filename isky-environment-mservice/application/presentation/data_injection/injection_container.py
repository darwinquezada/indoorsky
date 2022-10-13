from email import message
import os
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from dependency_injector import containers, providers
from application.data.repository_impl.environment_repository_impl import EnvironmentRepositoryImpl
from application.data.datasource.environment_datasource_impl import EnvironmentDatasourceImpl
from dotenv import load_dotenv
from flask import jsonify, abort

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)
   
class ApplicationContainer(containers.DeclarativeContainer):
    
        
    environment_datasource = providers.Factory(EnvironmentDatasourceImpl,
                                               database_name=os.environ['RDB_DB'],
                                               table_name=os.environ['RDB_TABLE'])
    
    environment_repository = providers.Factory(EnvironmentRepositoryImpl, 
                                               environment_datasource=environment_datasource())
