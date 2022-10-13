from email import message
import os
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from dependency_injector import containers, providers
from application.data.repository_impl.building_repository_impl import BuildingRepositoryImpl
from application.data.datasource.building_datasource_impl import BuildingDatasourceImpl
from dotenv import load_dotenv
from flask import jsonify, abort

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)
   
class ApplicationContainer(containers.DeclarativeContainer):
    
        
    building_datasource = providers.Factory(BuildingDatasourceImpl,
                                       database_name=os.environ['RDB_DB'],
                                       table_name=os.environ['RDB_TABLE'])
    
    building_repository = providers.Factory(BuildingRepositoryImpl,
                                            building_datasource=building_datasource())
