__all__ = 'BaseModel', 'DefaultBaseModel', 'ImmutableBaseModel', 'BaseConfig', 'const'

# TODO
#   check copy_on_model_validation

from pydantic import BaseModel as PydanticBaseModel, BaseSettings
from pydantic.main import ModelMetaclass
import orjson

from typing import Union, Optional, Generic, TypeVar, get_args
from sys import version_info
from os import getenv


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


T = TypeVar('T')

class const(Generic[T]): ...

class MyConfigMeta(ModelMetaclass):
    def __new__(cls, name, bases, attrs):

        def is_const(annotation):
            return getattr(annotation, '__origin__', None) is const

        def inner_type(annotation):
            return get_args(annotation)[0]

        constants = set()

        assert all(k in attrs for k, v in attrs.get('__annotations__', {}).items()
            if is_const(v)), 'you can\'t mark a field with no value as constant'

        for name, value in attrs.get('__annotations__', {}).items():
            if is_const(value):
                constants.add(name)
                attrs['__annotations__'][name] = inner_type(value)

        def __setattr__(self, name, value):
            if name in constants:
                raise TypeError(
                    f'{name} is constant, '
                    f'but you tried to override it with {value!r} of type {type(value).__name__!r}' +
                   (f' \n(check env variable {name!r} [case insensitive], it tries to override this constant)' 
                        if (env_var := getenv(name, None)) is not None
                        else ''))
            else:
                return super(BaseSettings, self).__setattr__(name, value)

        attrs['__setattr__'] = __setattr__
        attrs['__constants__'] = constants

        return super().__new__(cls, cls.__name__, bases, attrs)

class BaseConfig(BaseSettings, metaclass = MyConfigMeta):
    def __init__(self, *args, allow_env_vars_override_constants = False, **kwargs):
        from os import environ

        super().__init__(*args, **kwargs)

        try:
            assert not (will_override := {_.lower() for _ in self.__constants__ if _.lower() in environ})
        except AssertionError:
            if not allow_env_vars_override_constants:
                raise RuntimeError(f'env vars try to override constants: {", ".join(will_override)}')

    class Config:
        validate_all = True
        validate_assignment = True
        arbitrary_types_allowed = True