from email import message
import os
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from dependency_injector import containers, providers
from application.data.repository_impl.pos_tech_repository_impl import PosTechRepositoryImpl
from application.data.datasource.pos_tech_datasource_impl import PosTechDatasourceImpl
from dotenv import load_dotenv
from flask import jsonify, abort

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)
   
class ApplicationContainer(containers.DeclarativeContainer):
    
        
    pos_tech_datasource = providers.Factory(PosTechDatasourceImpl,
                                            database_name=os.environ['RDB_DB'],
                                            table_name=os.environ['RDB_TABLE'])
    
    pos_tech_repository = providers.Factory(PosTechRepositoryImpl,
                                            pos_tech_datasource=pos_tech_datasource())
