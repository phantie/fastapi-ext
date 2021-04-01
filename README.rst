my extension of FastAPI/Pydantic
-------------------

Examples:


.. code:: python


    from mypydantic import Model as DefaultBaseModel
    from myfastapi import MyFastAPI

    app = MyFastAPI()


    class UserOut(DefaultBaseModel):
        username: str
        items: list # equals to `items: list = []`
        misc: tuple[str, int] # equals to `misc: tuple[str, int] = ('', 0)`

    class UserIn(UserOut):
        password: str


    @app.post("/user/")
    def create_user(user: UserIn) -> UserOut:
        return UserOut.of(user) # equals to UserOut(**user.dict())

    # Equals to

    @app.post("/user/", response_model=UserOut)
    def create_user(user: UserIn):
        return UserOut.of(user)


    from fastapi.responses import PlainTextResponse

    @app.get('/plain-text/{text}')
    def get_plain_text(text: str) -> PlainTextResponse:
        return PlainTextResponse(content=text, media_type='text/html')

    # Equals to

    @app.get('/plain-text/{text}', response_class = PlainTextResponse)
    def get_plain_text(text: str):
        return PlainTextResponse(content=text, media_type='text/html')
