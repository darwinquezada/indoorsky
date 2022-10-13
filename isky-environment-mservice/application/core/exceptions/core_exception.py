import json
from werkzeug.exceptions import HTTPException


class BaseAPICode(HTTPException):
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

        super(BaseAPICode, self).__init__(message, None)

    def get_body(self, *args, **kwargs):
        body = {
            "code": self.error_code,
            "message": self.message,
        }
        text = json.dumps(body, ensure_ascii=False)
        return text

    def get_headers(self, *args, **kwargs):
        return [('Content-Type', 'application/json')]