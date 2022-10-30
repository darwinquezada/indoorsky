from email import message
import os
from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from dependency_injector import containers, providers
from application.data.repository_impl.audit_repository_impl import AuditRepositoryImpl
from application.data.datasource.audit_datasource_impl import AuditDatasourceImpl
from dotenv import load_dotenv
from flask import jsonify, abort

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)
   
class ApplicationContainer(containers.DeclarativeContainer):
    """
    Container for data injection
    """
    # Inject data (database name and table) to the datasource
    audit_datasource = providers.Factory(AuditDatasourceImpl,
                                       database_name=os.environ['RDB_DB'],
                                       table_name=os.environ['RDB_TABLE'])
    # Inject data to the implementation of the audit repository
    audit_repository = providers.Factory(AuditRepositoryImpl,
                                         audit_datasource=audit_datasource())
