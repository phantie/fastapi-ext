__all__ = 'FastAPI', 'APIRouter'


from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse, Response, JSONResponse

class BaseAPIMeta(type):
    def __new__(cls, name, bases, attrs):
        meths = 'get post delete put patch options trace head'

        def generate_method(meth_name):
            def wrap(self, path, **kwargs):
                meth = getattr(super(self.__class__, self), meth_name)
                def wrap(f):
                    if 'response_model' in kwargs and 'response_class' in kwargs:
                        raise ValueError('don\'t override response_model and response_class at once')
                    elif ('response_model' in kwargs or 'response_class' in kwargs) and \
                            'return' in getattr(f, '__annotations__', {}):
                        raise ValueError('either ambiguity or override')

                    response_model_or_class = (
                        getattr(f, '__annotations__', {})
                            .get('return', kwargs
                                .get('response_model', kwargs
                                    .get('response_class', 
                                        ORJSONResponse))))

                    if issubclass(response_model_or_class, Response):
                        kwargs['response_class'] = response_model_or_class
                    else:
                        kwargs['response_model'] = response_model_or_class
                        kwargs['response_class'] = ORJSONResponse

                    responses = kwargs.get('responses', {})

                    if responses and not isinstance(responses, dict):
                        kwargs['responses'] = responses.to_response_fmt()
                    return meth(path, **kwargs)(f)
                return wrap
            return wrap

        attrs.update({meth_name: generate_method(meth_name) for meth_name in meths.split()})

        return super().__new__(cls, name, bases, attrs)


class FastAPI(FastAPI, metaclass=BaseAPIMeta): ...

class APIRouter(APIRouter, metaclass=BaseAPIMeta): ...