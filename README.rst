# my extension of FastAPI/Pydantic


Examples:


.. code:: python


    from mypydantic import Model as BaseModel
    from myfastapi import MyFastAPI

    app = MyFastAPI()

    class UserOut(BaseModel):
        username: str
        items: List # equals to `items: List = []`

    class UserIn(UserOut):
        password: str

    @app.post("/user/")
    def create_user(user: UserIn) -> UserOut:
        return user

    # Equals to

    @app.post("/user/", response_model=UserOut)
    def create_user(user: UserIn):
        return user
