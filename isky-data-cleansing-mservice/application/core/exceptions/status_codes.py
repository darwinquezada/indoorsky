import code
from .core_exception import BaseAPICode


# Succesful code
class SuccessCode(BaseAPICode):
    code = 200
    message = "Success!"
     

class CreateSuccessCode(BaseAPICode):
    code = 201
    message = "Succesfully created."
    
    
class DeleteSuccessCode(BaseAPICode):
    code = 201
    message = "Succesfully removed."

    