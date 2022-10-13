from email import message
import os
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from dependency_injector import containers, providers
from application.data.repository_impl.wifi_repository_impl import WifiRepositoryImpl
from application.data.datasource.wifi_datasource_impl import WifiDatasourceImpl
from dotenv import load_dotenv
from flask import jsonify, abort

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)
   
class ApplicationContainer(containers.DeclarativeContainer):
    
        
    wifi_datasource = providers.Factory(WifiDatasourceImpl,
                                       database_name=os.environ['RDB_DB'],
                                       table_name=os.environ['RDB_TABLE'])
    
    wifi_repository = providers.Factory(WifiRepositoryImpl,
                                            wifi_datasource=wifi_datasource())
