__all__ = 'MyFastAPI', 'MyAPIRouter'

from tools import responses

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
                        if ('response_model' in kwargs) + ('response_class' in kwargs) == 2:
                            raise ValueError('')
                        elif ('response_model' in kwargs) + ('response_class' in kwargs) == 1 and \
                             'return' in getattr(f, '__annotations__', {}):
                            raise ValueError('')

                        response_model_or_class = (
                            getattr(f, '__annotations__', {})
                                .get('return', kwargs
                                    .get('response_model', kwargs
                                        .get('response_class', 
                                            ORJSONResponse))))

                        kwargs.__setitem__(
                            'response_class' if response_model_or_class in responses else 'response_model',
                            response_model_or_class
                        )

                        return meth(
                                    path,
                                    **kwargs)(f)
                    return wrap
                return wrap

            attrs[meth_name] = bake_in(meth_name)
        return super().__new__(cls, name, bases, attrs)
    


class MyFastAPI(FastAPI, metaclass=BaseAPIMeta): ...

class MyAPIRouter(APIRouter, metaclass=BaseAPIMeta): ...