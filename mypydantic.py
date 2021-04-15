__all__ = 'BaseModel', 'ImmutableBaseModel', 'BaseConfig', 'Const', 'ImmutableConfig'

# TODO
#   check copy_on_model_validation

from pydantic import BaseModel as PydanticBaseModel, BaseSettings, Field
from pydantic.main import ModelMetaclass
import orjson

from typing import Union, Optional, Generic, TypeVar, get_args
from sys import version_info
from os import getenv
from functools import partial


class BaseModel(PydanticBaseModel):
    @classmethod
    def of(cls, of, **add): return cls(**of.dict(), **add)

    class Config:
        json_loads = orjson.loads
        json_dumps = lambda v, *, default: orjson.dumps(v, default=default).decode()

class ImmutableBaseModel(BaseModel):
    class Config:
        allow_mutation = False

class BaseConfigMeta(ModelMetaclass):
    def __new__(cls, name, bases, attrs):
        def const(annotation):
            from pydantic.fields import FieldInfo as FieldType
            return isinstance(annotation, FieldType) and not annotation.allow_mutation

        def set_const(annotation):
            from pydantic.fields import Undefined
            return not (annotation.default is Undefined or annotation.default is ...)

        attrs['__constants_with_default__'] = {
            name for name, value in attrs.items()
            if const(value) and set_const(value)}

        return super().__new__(cls, name, bases, attrs)

class BaseConfig(BaseSettings, metaclass = BaseConfigMeta):
    """
    Customized, more robust version of BaseSettings.
        Prevents silent bugs when 'allow_mutation' == False
        but env. vars try to override any of them.
    """

    def __init__(self, *args, allow_env_vars_override_constants = False, **kwargs):
        from os import environ
        if not allow_env_vars_override_constants and \
            (will_override := {const for const in self.__constants_with_default__ if const in environ}):
                raise RuntimeError(f'env vars try to override constants: {", ".join(will_override)}')

        super().__init__(*args, **kwargs)

    class Config:
        validate_all = True
        validate_assignment = True
        arbitrary_types_allowed = True

Const = partial(Field, allow_mutation=False)

class ImmutableConfig(BaseSettings):
    class Config:
        allow_mutation = False
        validate_all = True
        arbitrary_types_allowed = True