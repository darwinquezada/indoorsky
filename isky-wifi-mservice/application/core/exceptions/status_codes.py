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
    
class UpdateSuccessCode(BaseAPICode):
    code = 201
    message = "Succesfully updated."
    

# Error code
class NoExistCode(BaseAPICode):
    code = 404
    message = "Register does not exist."
    
class RecordExistCode(BaseAPICode):
    code = 409
    message = "Register already exists in the database."

class ErrorCode(BaseAPICode):
    code = 501
    message = "An error has ocurred."
    
