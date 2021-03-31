from mypydantic import ImmutableBaseModel, BaseModel

import pytest

def test_immut():
    class User(ImmutableBaseModel):
        name: str

    u = User(name = 'phantie')
    assert u.name == 'phantie'

    with pytest.raises(TypeError) as err:
        u.name = 'Alex'

    assert err.value.args[0] == '"User" is immutable and does not support item assignment'

def test_json():
    from pydantic import BaseModel as PydanticBaseModel
    class User(BaseModel):
        name: str
        age: int

    class PydanticUser(PydanticBaseModel):
        name: str
        age: int

    params = [('phantie', 20), ('', 0), ('55', 5), ('XD' * 20, 69 * 69)]

    for name, age in params:
        assert User(name=name, age=age).json() == \
            PydanticUser(name=name, age=age).json().replace(': ', ':').replace(', ', ',')