from mypydantic import BaseModel

from typing import *

import pytest

def test_basic():
    class User(BaseModel):
        username: str
        items: List[str]
        misc: Tuple

    user = User(usename = 'phantie')
    assert user.items == [] and user.misc == ()