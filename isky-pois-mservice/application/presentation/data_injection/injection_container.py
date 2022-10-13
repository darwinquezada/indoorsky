from email import message
import os
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from dependency_injector import containers, providers
from application.data.repository_impl.poi_repository_impl import PoiRepositoryImpl
from application.data.datasource.poi_datasource_impl import PoiDatasourceImpl
from dotenv import load_dotenv
from flask import jsonify, abort

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)
   
class ApplicationContainer(containers.DeclarativeContainer):
    
        
    poi_datasource = providers.Factory(PoiDatasourceImpl,
                                       database_name=os.environ['RDB_DB'],
                                       table_name=os.environ['RDB_TABLE'])
    
    poi_repository = providers.Factory(PoiRepositoryImpl,
                                       poi_datasource=poi_datasource())
