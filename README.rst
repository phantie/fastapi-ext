my extension of FastAPI/Pydantic
-------------------

Examples:


.. code:: python


    from mypydantic import BaseModel, ImmutableModel
    from myfastapi import FastAPI
    from jsonable_error import ErrorFactory
    from fastapi.responses import PlainTextResponse


    app = FastAPI()

    FORBIDDEN = ErrorFactory('Access denied', http_code = 403)
    USER_NOT_FOUND = ErrorFactory('User not found', code = 50, http_code = 404) # Twitter style error responses


    class UserOut(BaseModel):
        username: str

    class UserIn(UserOut):
        password: str


    @app.post("/user/")
    def create_user(user: UserIn) -> UserOut:
        return UserOut.of(user) # equals to UserOut(**user.dict())

    # Equals to

    @app.post("/user/", response_model=UserOut)
    def create_user(user: UserIn):
        return UserOut.of(user)


    @app.get('/plain-text/{text}', responses = FORBIDDEN) # generates great documentation, look at the example below
    def get_plain_text(text: str) -> PlainTextResponse:
        if bad_mood:
            return FORBIDDEN.respond()

        return PlainTextResponse(content=text, media_type='text/html')

    # Equals to

    class ErrorBody(ImmutableModel):
        message: str
        code: int

    class ErrorResponse(ImmutableModel):
        error: ErrorBody = ErrorBody(message = 'Access denied', code = 403)

    @app.get(
        '/plain-text/{text}',
        response_class = PlainTextResponse,
        responses = {403: {'model': ErrorResponse}}) 
    def get_plain_text(text: str):
        if bad_mood:
            return ORJSONResponse(content={'error': {'message': 'Access denied', 'code': 403}}, status_code = 403)

        return PlainTextResponse(content=text, media_type='text/html')

    # You can even group it together if they don't have duplicate http codes underneath
    @app.get('/', responses = USER_NOT_FOUND | FORBIDDEN)
    def index():
        if bad_mood:
            return FORBIDDEN.respond('NOT T.O.D.A.Y')
        if not in_db(user_id):
            return USER_NOT_FOUND.respond(f'User with id {user_id} not found')
        return {'message': 'Hll wrld!'}