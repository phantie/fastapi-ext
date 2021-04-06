from mypydantic import BaseModel, ImmutableBaseModel

from typing import *
from collections import defaultdict, deque, OrderedDict as ordereddict

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


    for Model in models:
        class UserOut(Model):
            username: str

        class UserIn(UserOut):
            password: str

        user = UserIn(username='phantie')
        assert UserOut.of(user) == UserOut(**user.dict())