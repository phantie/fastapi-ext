from mypydantic import BaseModel
import pytest

def test_basic():
    class User(BaseModel):
        username: str
        items: list[str]
        misc: tuple

    user = User(usename = 'phantie')
    assert user.items == [] and user.misc == ()