def group_kwargs(f):
    """ Groups parameters passed by keyword, merges with defaults,
        and passes the dict as a first argument to a function

        @group_kwargs
        def foo(grouped, bar, /, baz, *, a=1, b=2, c=3):
            return grouped
        
        assert foo(bar, baz = 0, c = 42) == {'a':1, 'b': 2, 'c': 42, 'baz': 0}
       """

    def wrap(*args, **kwargs):
        def get_defaults_with_names(f):
            from inspect import signature, _empty, Parameter
            return dict((name, par.default) for name, par in signature(f).parameters.items() 
                            if (par.kind == Parameter.POSITIONAL_OR_KEYWORD or
                                par.kind == Parameter.KEYWORD_ONLY) and
                                par.default is not _empty)

        updated = {**get_defaults_with_names(f), **kwargs}
        return f(updated, *args, **kwargs)
    return wrap