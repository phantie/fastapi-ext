from mypydantic import BaseModel, ImmutableBaseModel
import pytest

models = (BaseModel, ImmutableBaseModel)


def test_of():
    for Model in models:

        class BaseUser(Model):
            name: str

        class User(BaseUser):
            password: str

        u = BaseUser(name='phantie')

        assert User.of(u, password = 'gibberish') == User(**u.dict(), password = 'gibberish')