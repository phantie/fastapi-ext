from pydantic import BaseModel
from pydantic.main import ModelMetaclass

from typing import Union, Optional
from sys import version_info

if version_info >= (3, 9, 0):
    from types import GenericAlias
else:
    from typing import _GenericAlias as GenericAlias

class BaseMeta(ModelMetaclass):
    def __new__(cls, name, bases, attrs):
        annotations = attrs.get('__annotations__', {})

        for key in set(annotations).difference(set(attrs)):
            value = annotations[key]

            if isinstance(value, GenericAlias):
                origin = value.__origin__
                if origin is Union:
                    pass
                else:
                    attrs[key] = origin()
            else:
                attrs[key] = value()

        return super().__new__(cls, cls.__name__, (BaseModel, object), attrs)

class Model(metaclass=BaseMeta): ...