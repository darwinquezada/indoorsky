from application.domain.respositories.verify_token import VerifyToken
from application.data.data_sources.datasource import IDataSource

class VerifyTokenImpl(VerifyToken):
    def __init__(self, datasource: IDataSource) -> None:
        self.datasource = datasource
    
    def verify(self, endpoint: str, project_id: str, jwt_token: str) -> dict:
        return self.datasource.verify_token(endpoint=endpoint, 
                                             project_id=project_id, 
                                             jwt_token=jwt_token)
        