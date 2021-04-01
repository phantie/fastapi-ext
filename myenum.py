__all__ = 'UniqueEnum',

from enum import Enum, EnumMeta


class MyEnumMeta(EnumMeta):
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, cls.__name__, bases, attrs)
        values = tuple(var.value for var in new_class._member_map_.values())
        if len(values) != len(set(values)):
            raise ValueError(f"duplicate values found in <enum '{name}'>")
        return new_class

class UniqueEnum(Enum, metaclass=MyEnumMeta): ...