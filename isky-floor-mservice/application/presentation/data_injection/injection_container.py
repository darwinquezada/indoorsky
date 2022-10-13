from email import message
import os
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from dependency_injector import containers, providers
from application.data.repository_impl.floor_repository_impl import FloorRepositoryImpl
from application.data.datasource.floor_datasource_impl import FloorDatasourceImpl
from dotenv import load_dotenv
from flask import jsonify, abort

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)
   
class ApplicationContainer(containers.DeclarativeContainer):
    
        
    floor_datasource = providers.Factory(FloorDatasourceImpl,
                                       database_name=os.environ['RDB_DB'],
                                       table_name=os.environ['RDB_TABLE'])
    
    floor_repository = providers.Factory(FloorRepositoryImpl,
                                         floor_datasource=floor_datasource())
