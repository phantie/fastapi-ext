__all__ = 'group_kwargs',


from functools import partial, wraps
from inspect import signature

def group_kwargs(f = None, /, exclude = None, include = None):
    """ Groups parameters passed by keyword, merges with defaults,
        and passes the dict as a first argument to a function

        @group_kwargs
        def foo(grouped, bar, /, baz, *, a=1, b=2, c=3):
            return grouped
        
        assert foo(bar, baz = 0, c = 42) == {'a':1, 'b': 2, 'c': 42, 'baz': 0}
       """

    assert not (exclude is not None and include is not None)

    if f is None:
        if exclude is not None:
            return partial(group_kwargs, exclude = exclude)
        if include is not None:
            return partial(group_kwargs, include = include)

    @wraps(f)
    def wrap(*args, **kwargs):
        def get_defaults_with_names(f):
            from inspect import signature, _empty, Parameter
            result = dict((name, par.default) for name, par in signature(f).parameters.items() 
                            if (par.kind == Parameter.POSITIONAL_OR_KEYWORD or
                                par.kind == Parameter.KEYWORD_ONLY) and
                                par.default is not _empty)

            if exclude is not None:
                assert all(ex in result for ex in exclude)
                result = {k: v for k, v in result.items() if k not in exclude}
            if include is not None:
                assert all(ex in result for ex in include)
                result = {k: v for k, v in result.items() if k in include}

            return result

        updated = {**get_defaults_with_names(f), **kwargs}
        return f(updated, *args, **kwargs)

    sig = signature(f)
    wrap.__signature__ = sig.replace(parameters=tuple(sig.parameters.values())[1:])

    return wrap