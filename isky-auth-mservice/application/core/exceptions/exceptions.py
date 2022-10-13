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


class ContentTypeException(BaseAPIException):
    error_code = -2
    message = "Unsupported content-type"


class ParameterException(BaseAPIException):
    error_code = 1002
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
    message = "User not activated"


class AuthException(BaseAPIException):
    error_code = 2005
    message = "Authentication failed, token not found"


class InvalidTokenException(BaseAPIException):
    error_code = 2006
    message = "Invalid token"


class ExpiredTokenException(BaseAPIException):
    error_code = 2007
    message = "Toke expired."


class EmailExistException(BaseAPIException):
    error_code = 2008
    message = "Email has been registered."


class RefreshException(BaseAPIException):
    error_code = 2009
    message = "Failed to update token."
    
    
class TokenNotProvidedException(BaseAPIException):
    error_code = 2010
    message = "No token provided."


class ResourceNotExistException(BaseAPIException):
    error_code = 4001
    message = "Resource does not exist."


class ResourceExistException(BaseAPIException):
    error_code = 4002
    message = "Resource already exist."
