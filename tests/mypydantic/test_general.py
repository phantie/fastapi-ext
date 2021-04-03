from mypydantic import *

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

def test_my_config_const():
    ### to make the test stable
    from os import environ
    environ['username'] = 'phantie'
    ###

    class Config(BaseConfig):
        username = 'phantie'
        password: const[int] = 21
        

    config = Config()

    assert config.username == 'phantie' and config.password == 21


    config.username = 'povar'
    with pytest.raises(TypeError) as err:
        config.password = 13

    assert 'is constant' in err.value.args[0]

    assert config.username == 'povar' and config.password == 21
