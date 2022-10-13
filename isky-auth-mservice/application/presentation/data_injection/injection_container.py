import os
from dependency_injector import containers, providers
from application.data.data_sources.datasource_impl import DataSourceImpl
from application.data.repository_impl.verify_token_impl import VerifyTokenImpl

from dotenv import load_dotenv

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)

class ApplicationContainer(containers.DeclarativeContainer):
   parameters = {
   'endpoint': os.environ['APPWRITEENDPOINT'],
   'project_id': os.environ['APPWRITEPROJECTID']
   }
   
   datasource = providers.Singleton(DataSourceImpl)
   repository = providers.Factory(VerifyTokenImpl, datasource=datasource)
