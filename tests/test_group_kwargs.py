from arg_group import group_kwargs

def test_case1():
    @group_kwargs
    def foo(grouped, *, a=1, b=2, c=3):
        return grouped

    assert foo() == {'a':1, 'b': 2, 'c': 3}

def test_case2():
    @group_kwargs
    def foo(grouped, bar, baz, *, a=1, b=2, c=3):
        return grouped

    for bar, baz in [(1, 2), ('', b''), (object, type)]:
        assert foo(bar, baz) == {'a':1, 'b': 2, 'c': 3}

def test_case3():
    @group_kwargs
    def foo(grouped, bar, /, baz, *, a=1, b=2, c=3):
        return grouped

    for bar, baz in [(1, 2), ('', b''), (object, type)]:
        assert foo(bar, baz = baz) == {'a':1, 'b': 2, 'c': 3, 'baz': baz}

    assert foo(bar, baz = 0, c = 42) == {'a':1, 'b': 2, 'c': 42, 'baz': 0}