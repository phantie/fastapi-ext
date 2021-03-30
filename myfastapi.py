from fastapi import FastAPI

__all__ = ['MyFastAPI']


class MyFastAPIMeta(type):
    def __new__(cls, name, bases, attrs):
        meths = 'get post delete put patch options trace head'

        for meth_name in meths.split():
            def bake_in(meth_name):
                def wrap(self, path, **kwargs):
                    meth = getattr(super(self.__class__, self), meth_name)
                    def wrap(f):
                        response_model = (
                            getattr(f, '__annotations__', {}).get('return', kwargs.pop('response_model', None)))
                        return meth(path, **kwargs, response_model=response_model)(f)
                    return wrap
                return wrap

            attrs[meth_name] = bake_in(meth_name)
        return super().__new__(cls, name, bases, attrs)
    


class MyFastAPI(FastAPI, metaclass=MyFastAPIMeta):
    pass
