from mypydantic import BaseModel

from typing import *
from collections import defaultdict, deque, OrderedDict as ordereddict

import pytest

def test_basic():
    class User(BaseModel):
        username: str
        items: List[str]
        misc: Tuple

    user = User(usename = 'phantie')
    assert user.items == [] and user.misc == ()

def test_types():

    class Foo(BaseModel):
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

def test_hinted_types():
    from collections import deque, defaultdict, OrderedDict
    class Foo(BaseModel):
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