from pydantic import BaseModel as PydanticBaseModel
from pydantic.main import ModelMetaclass
import orjson

from typing import Union, Optional
from sys import version_info

if version_info >= (3, 9, 0):
    from types import GenericAlias
else:
    from typing import _GenericAlias as GenericAlias


__all__ = 'BaseModel', 'DefaultBaseModel', 'ImmutableBaseModel'



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