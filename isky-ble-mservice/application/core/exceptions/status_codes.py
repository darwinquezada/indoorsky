from .core_exception import BaseAPICode


# Success code
# 2XX response codes
class SuccessResponseCode(BaseAPICode):
    code = 200
    message = "Success!"
     
class CreatedResponseCode(BaseAPICode):
    message = "Successfully created."
    code = 201
    
class AcceptedResponseCode(BaseAPICode):
    code = 202
    message = "Request accepted successfully."
    
class UpdateResponseCode(BaseAPICode):
    code = 204
    message = "Record updated successfully."
    
class DeletedResponseCode(BaseAPICode):
    code = 204
    message = "Record removed successfully."
    
# 3XX response codes
class MovedPermanentlyResponseCode(BaseAPICode):
    code = 301
    message = "Resource moved permanently."
    
class NotModifiedResponseCode(BaseAPICode):
    code = 304
    message = "Resource not modified."
    
# 4XX response codes
class BadResponseCode(BaseAPICode):
    code = 400
    message = "Bad request."
    
class UnauthorizedResponseCode(BaseAPICode):
    code = 401
    message = "Unauthorized."
    
class ForbiddenResponseCode(BaseAPICode):
    code = 403
    message = "Forbidden."
    
class NotFoundResponseCode(BaseAPICode):
    code = 404
    message = "Not Found."
    
class MethodNotAllowedResponseCode(BaseAPICode):
    code = 405
    message = "Method not allowed."

class ConflictResponseCode(BaseAPICode):
    code = 409
    message = "Conflict."

# 5XX response codes
class InternalServerErrorResponseCode(BaseAPICode):
    code = 500
    message = "Internal server error."
    
class NotImplementedResponseCode(BaseAPICode):
    code = 501
    message = "Not implemented."
    
class ServiceUnavailableResponseCode(BaseAPICode):
    code = 503
    message = "The server is not ready to handle the request."
    
    