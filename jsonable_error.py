from collections import defaultdict

from pydantic import ImmutableBaseModel as Model
from pydantic import Field, PositiveInt, validator
from pydantic.main import ModelMetaclass

from fastapi.responses import ORJSONResponse
import starlette


status_codes = {getattr(starlette.status, name) for name in dir(starlette.status) if name.startswith('HTTP')}
http_code_to_error_responses = defaultdict(list)
error_response_to_http_code = dict()


class ErrorBody(Model):
    message: str
    code: int

    @validator('code')
    def validate_code(cls, code):
        if not (400 <= code < 600) and code in status_codes:
            raise ValueError('don`t create ambiguity using non error http code as an internal code')
        return code

    def __init__(self, message, **kwargs):
        super().__init__(message = message, **kwargs)

    class Config:
        validate_all = True

class ErrorResponseList(list):
    _arleady_used_names = set()
    _arleady_used_codes = set()

    def append(self, el):
        assert issubclass(el, Error)
        assert el.__name__ not in self._arleady_used_names
        http_code = error_response_to_http_code[el]
        
        if http_code in self._arleady_used_codes:
            raise ValueError('set of errors responses must not have duplicate http codes underneath')
        
        self._arleady_used_codes.append(http_code)
        self._arleady_used_names.append(el.__name__)
        super().append(el)

    def __or__(self, another):
        self.append(another)
        return self

    def to_response_fmt(self):
        return {error_response_to_http_code[er]: {'model': er} for er in self}


class ErrorMeta(ModelMetaclass):
    def __or__(cls, another):
        return ErrorResponseList((cls, another))

    def __repr__(cls):
        return f"ErrorResponse({cls.__fields__['error'].default})"


class Error(Model, metaclass = ErrorMeta):

    error: ErrorBody

    def __init__(self, message, **kwargs):
        body = ErrorBody(message, **kwargs)
        super().__init__(error = body)


class ErrorFactory:

    def __new__(cls, message, *, http_code, code = None):
        code = code or http_code

        class ServiceError(Error): 
            error = ErrorBody(message, code = code)

            @classmethod
            def respond(cls, message = message):
                content = cls(message, code = code).dict()
                content['error']['message'] = message
                return ORJSONResponse(content=content, status_code = http_code)

            @classmethod
            def to_response_fmt(cls):
                return {error_response_to_http_code[cls]: {'model': cls}}

        ServiceError.http_code = http_code

        http_code_to_error_responses[http_code].append(ServiceError)
        error_response_to_http_code[ServiceError] = http_code

        ServiceError.__name__ = ''.join(_.title() for _ in message.split())

        return ServiceError