from mypydantic import BaseModel, DefaultBaseModel

from typing import *
from collections import defaultdict, deque, OrderedDict as ordereddict

import pytest


models = (BaseModel, DefaultBaseModel)


def test_default_basic():
    class User(DefaultBaseModel):
        username: str
        items: List[str]
        misc: Tuple

    user = User(usename = 'phantie')
    assert user.items == [] and user.misc == ()

def test_default_types():

    class Foo(DefaultBaseModel):
        fs: FrozenSet
        t: Tuple
        l: List
        d: Dict
        dd: DefaultDict
        dq: Deque
        od: OrderedDict


    a = Foo().__getattribute__
    assert a('fs') == frozenset()
    assert a('t') == tuple()
    assert a('l') == list()
    assert a('d') == dict()
    assert a('dd') == defaultdict()
    assert a('dq') == deque()
    assert a('od') == ordereddict()

def test_default_hinted_types():
    from collections import deque, defaultdict, OrderedDict
    class Foo(DefaultBaseModel):
        fs: FrozenSet[int]
        t: Tuple[int, str, bytes]
        l: List[float]
        d: Dict[str, int]
        dd: DefaultDict[str, int]
        dq: Deque[int]
        # od: OrderedDict[str, float] # does not work with OrderedDict


    a = Foo().__getattribute__
    assert a('fs') == frozenset()
    assert a('t') == (0, '', b'')
    assert a('l') == list()
    assert a('d') == dict()
    assert a('dd') == defaultdict()
    assert a('dq') == deque()

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