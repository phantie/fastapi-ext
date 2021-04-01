__all__ = 'UniqueEnum',

from enum import Enum, EnumMeta


class MyEnumMeta(EnumMeta):
    def __new__(cls, name, bases, attrs):
        from tools import unique_seq

        new_class = super().__new__(cls, cls.__name__, bases, attrs)
        values = tuple(var.value for var in new_class._member_map_.values())
        if not unique_seq(values):
            raise ValueError(f"duplicate values found in <enum '{name}'>")
        return new_class

class UniqueEnum(Enum, metaclass=MyEnumMeta): ...