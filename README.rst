# my extension of FastAPI/Pydantic


Examples:


.. code:: python


    from mypydantic import Model as BaseModel
    from myfastapi import MyFastAPI

    app = MyFastAPI()

    class UserOut(BaseModel):
        username: str
        items: list # equals to `items: ... = []`
        misc: tuple[str, int, bytes] # equals to `misc: ... = ('', 0, b'')`

    class UserIn(UserOut):
        password: str

    @app.post("/user/")
    def create_user(user: UserIn) -> UserOut:
        return user

    # Equals to

    @app.post("/user/", response_model=UserOut)
    def create_user(user: UserIn):
        return user
