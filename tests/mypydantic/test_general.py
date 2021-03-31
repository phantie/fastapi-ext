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