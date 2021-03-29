from mypydantic import BaseModel
import pytest


def test_basic():
    class User(BaseModel):
        username: str
        items: list[str]
        misc: tuple

    user = User(usename = 'phantie')
    assert user.items == [] and user.misc == ()

def test_types():
    from collections import deque, defaultdict, OrderedDict
    class Foo(BaseModel):
        fs: frozenset
        t: tuple
        l: list
        d: dict
        dd: defaultdict
        dq: deque
        od: OrderedDict


    a = Foo().__getattribute__
    assert a('fs') == frozenset()
    assert a('t') == tuple()
    assert a('l') == list()
    assert a('d') == dict()
    assert a('dd') == defaultdict()
    assert a('dq') == deque()
    assert a('od') == OrderedDict()


def test_hinted_types():
    from collections import deque, defaultdict, OrderedDict
    class Foo(BaseModel):
        fs: frozenset[int]
        t: tuple[int, str, bytes]
        l: list[float]
        d: dict[str, int]
        dd: defaultdict[str, int]
        dq: deque[int]
        od: OrderedDict[str, float]


    a = Foo().__getattribute__
    assert a('fs') == frozenset()
    assert a('t') == (0, '', b'')
    assert a('l') == list()
    assert a('d') == dict()
    assert a('dd') == defaultdict()
    assert a('dq') == deque()
    assert a('od') == OrderedDict()