__all__ = 'MyFastAPI', 'MyAPIRouter'

from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse


class BaseAPIMeta(type):
    def __new__(cls, name, bases, attrs):
        meths = 'get post delete put patch options trace head'

        for meth_name in meths.split():
            def bake_in(meth_name):
                def wrap(self, path, **kwargs):
                    meth = getattr(super(self.__class__, self), meth_name)
                    def wrap(f):
                        response_model = (
                            getattr(f, '__annotations__', {}).get('return', kwargs.pop('response_model', None)))
                        return meth(
                                    path,
                                    **kwargs,
                                    response_model=response_model,
                                    response_class=ORJSONResponse)(f)
                    return wrap
                return wrap

            attrs[meth_name] = bake_in(meth_name)
        return super().__new__(cls, name, bases, attrs)
    


class MyFastAPI(FastAPI, metaclass=BaseAPIMeta): ...

class MyAPIRouter(APIRouter, metaclass=BaseAPIMeta): ...