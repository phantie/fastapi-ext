__all__ = 'BaseModel', 'DefaultBaseModel', 'ImmutableBaseModel', 'BaseConfig', 'Const', 'ImmutableConfig'

# TODO
#   check copy_on_model_validation

from pydantic import BaseModel as PydanticBaseModel, BaseSettings, Field
from pydantic.main import ModelMetaclass
import orjson

from typing import Union, Optional, Generic, TypeVar, get_args
from sys import version_info
from os import getenv
from functools import partial


if version_info >= (3, 9, 0):
    from types import GenericAlias
else:
    from typing import _GenericAlias as GenericAlias


class BaseModel(PydanticBaseModel):
    @classmethod
    def of(cls, of, **add): return cls(**of.dict(), **add)

    class Config:
        json_loads = orjson.loads
        json_dumps = lambda v, *, default: orjson.dumps(v, default=default).decode()


class DefaultBaseMeta(ModelMetaclass):
    def __new__(cls, name, bases, attrs):
        annotations = attrs.get('__annotations__', {})

        for key in set(annotations).difference(set(attrs)):
            value = annotations[key]

            if isinstance(value, GenericAlias):
                origin = value.__origin__
                if origin is Union:
                    pass
                elif origin is tuple:
                    attrs[key] = tuple(default() for default in value.__args__)
                else:
                    attrs[key] = origin()
            else:
                attrs[key] = value()

        return super().__new__(cls, cls.__name__, (BaseModel, object), attrs)

class DefaultBaseModel(metaclass=DefaultBaseMeta): ...

class ImmutableBaseModel(BaseModel):
    class Config:
        allow_mutation = False

class MyConfigMeta(ModelMetaclass):
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

class BaseConfig(BaseSettings, metaclass = MyConfigMeta):
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
        validate_assignment = True
        arbitrary_types_allowed = True