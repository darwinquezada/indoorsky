
from .core_exception import BaseAPICode


class UnknownException(BaseAPICode):
    code = 500


class AuthException(BaseAPICode):
    error_code = 401
    message = "Failed to verify JWT. Invalid token: Incomplete segments."
    
    
class ConnectionException(BaseAPICode):
    error_code = 404
    message = "Cannot connect to the authentication service."

    
class ContentTypeException(BaseAPICode):
    error_code = -2
    message = "Unsupported content-type"


class ParameterException(BaseAPICode):
    error_code = 2000
    message = "Parameter error"


class UserExistException(BaseAPICode):
    error_code = 2001
    message = "User already exist"


class UserNotExistException(BaseAPICode):
    error_code = 2002
    message = "User not exist"


class PasswordException(BaseAPICode):
    error_code = 2003
    message = "Password error"


class ActiveException(BaseAPICode):
    error_code = 2004
    message = "User not active"


class EmailExistException(BaseAPICode):
    error_code = 2005
    message = "Email has been registered."


class InvalidTokenException(BaseAPICode):
    error_code = 3001
    message = "Invalid token"


class ExpiredTokenException(BaseAPICode):
    error_code = 3002
    message = "Toke expired."


class RefreshException(BaseAPICode):
    error_code = 3003
    message = "Failed to update token."
    
    
class TokenNotProvidedException(BaseAPICode):
    error_code = 3004
    message = "No token provided."


class ResourceNotExistException(BaseAPICode):
    error_code = 4001
    message = "Resource does not exist."


class ResourceExistException(BaseAPICode):
    error_code = 4002
    message = "Resource already exist."
    