from mypydantic import *

from os import environ

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

@pytest.mark.skipif('password' in environ, reason='Depends on env var')
def test_my_config_const():
    from pydantic import Field
    ### to make the test stable
    from os import environ
    environ['username'] = 'joojoo'
    ###

    class Config(BaseConfig):
        username: str = Field('phantie', allow_mutation = False)
        password: int = Field(21, allow_mutation = False)


    with pytest.raises(RuntimeError):
        config = Config(allow_env_vars_override_constants=False)
    config = Config(allow_env_vars_override_constants=True)

    assert config.username == 'joojoo' and config.password == 21

    with pytest.raises(TypeError) as err:
        config.password = 13
    with pytest.raises(TypeError) as err:
        config.username = 'povar'


    assert config.username == 'joojoo' and config.password == 21

def test_my_config_const_with_unset():
    from pydantic import Field
    ### to make the test stable
    from os import environ
    environ['not_yet_set'] = '100'
    ###

    class Config(BaseConfig):
        not_yet_set: str = Field(..., allow_mutation=False)
        # it allows env vars to override this value without panicking

    config = Config()

    assert config.not_yet_set == '100'

    with pytest.raises(TypeError) as err:
        config.not_yet_set = '1001'

    assert config.not_yet_set == '100'

@pytest.mark.skipif(any(var in environ for var in ('rand', 'domain', 'port', 'secret')),
    reason='Depends on env vars')
def test_subconfigs():

    class SubConfig(BaseConfig):
        domain: str = Const('mail.google.com')
        port: int = Const(123)
        rand: bool = True

    class Config(BaseConfig):
        secret: str = Const('SECRET')

        mailing = SubConfig()

    config = Config()

    config.mailing.rand = False
    with pytest.raises(TypeError):
        config.mailing.domain = 'api.hooli.inc'

    assert config.mailing.rand == False and config.mailing.domain == 'mail.google.com'
