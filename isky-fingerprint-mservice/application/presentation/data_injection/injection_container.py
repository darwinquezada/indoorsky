import os
from dependency_injector import containers, providers
from application.data.repository_impl.fingerprint_repository_impl import FingerprintRepositoryImpl
from application.data.datasource.fingerprint_datasource_impl import FingerprintDatasourceImpl
from dotenv import load_dotenv

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)
   
class ApplicationContainer(containers.DeclarativeContainer):
    
        
    fingerprint_datasource = providers.Factory(FingerprintDatasourceImpl,
                                       database_name=os.environ['RDB_DB'],
                                       table_name=os.environ['RDB_TABLE'])
    
    fingerprint_repository = providers.Factory(FingerprintRepositoryImpl,
                                         fingerprint_datasource=fingerprint_datasource())
