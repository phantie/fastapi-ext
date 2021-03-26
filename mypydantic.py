from pydantic import BaseModel
from pydantic.main import ModelMetaclass

from typing import Union, Optional

class NewMeta(type):
    def __new__(cls, name, bases, attrs):
        annotations = attrs.get('__annotations__', {})

        for maybe_optional_key in set(annotations).difference(set(attrs)):
            maybe_optional = annotations[maybe_optional_key]

            if getattr(maybe_optional, '__origin__', None) is Union and \
                getattr(maybe_optional, '__args__') is not None and \
                    type(None) in getattr(maybe_optional, '__args__', []):

                attrs[maybe_optional_key] = None

        return type(cls.__name__, (BaseModel, object), attrs)

class Model(metaclass=NewMeta): ...