from mypydantic import BaseModel, DefaultBaseModel, ImmutableBaseModel
import pytest

models = (BaseModel, DefaultBaseModel, ImmutableBaseModel)


def test_default_basic():
    class User(DefaultBaseModel):
        username: str
        items: list[str]
        misc: tuple

    user = User(usename = 'phantie')
    assert user.items == [] and user.misc == ()

def test_default_types():
    from collections import deque, defaultdict, OrderedDict
    class Foo(DefaultBaseModel):
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


def test_default_hinted_types():
    from collections import deque, defaultdict, OrderedDict
    class Foo(DefaultBaseModel):
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

def test_of():
    for Model in models:

        class BaseUser(Model):
            name: str

        class User(BaseUser):
            password: str

        u = BaseUser(name='phantie')

        assert User.of(u, password = 'gibberish') == User(**u.dict(), password = 'gibberish')