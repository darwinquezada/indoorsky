import json

from werkzeug.exceptions import HTTPException


class BaseAPIException(HTTPException):
    code = 200
    error_code = -1
    message = 'exception'

    def __init__(self, code=None, message=None, error_code=None, headers=None):
        if code:
            self.code = code
        if message:
            self.message = message
        if error_code:
            self.error_code = error_code
        if headers is not None:
            headers_merged = headers.copy()
            headers_merged.update(headers)
            self.headers = headers_merged

        super(BaseAPIException, self).__init__(message, None)

    def get_body(self, *args, **kwargs):
        body = {
            "code": self.error_code,
            "message": self.message,
        }
        text = json.dumps(body, ensure_ascii=False)
        return text

    def get_headers(self, *args, **kwargs):
        return [('Content-Type', 'application/json')]


class UnknownException(BaseAPIException):
    code = 500


class AuthException(BaseAPIException):
    error_code = 401
    message = "Failed to verify JWT. Invalid token: Incomplete segments."
    
    
class ConnectionException(BaseAPIException):
    error_code = 404
    message = "Cannot connect to the authentication service."

    
class ContentTypeException(BaseAPIException):
    error_code = -2
    message = "Unsupported content-type"


class ParameterException(BaseAPIException):
    error_code = 2000
    message = "Parameter error"


class UserExistException(BaseAPIException):
    error_code = 2001
    message = "User already exist"


class UserNotExistException(BaseAPIException):
    error_code = 2002
    message = "User not exist"


class PasswordException(BaseAPIException):
    error_code = 2003
    message = "Password error"


class ActiveException(BaseAPIException):
    error_code = 2004
    message = "User not active"


class EmailExistException(BaseAPIException):
    error_code = 2005
    message = "Email has been registered."


class InvalidTokenException(BaseAPIException):
    error_code = 3001
    message = "Invalid token"


class ExpiredTokenException(BaseAPIException):
    error_code = 3002
    message = "Toke expired."


class RefreshException(BaseAPIException):
    error_code = 3003
    message = "Failed to update token."
    
    
class TokenNotProvidedException(BaseAPIException):
    error_code = 3004
    message = "No token provided."


class ResourceNotExistException(BaseAPIException):
    error_code = 4001
    message = "Resource does not exist."


class ResourceExistException(BaseAPIException):
    error_code = 4002
    message = "Resource already exist."
    