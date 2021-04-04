from mypydantic import BaseConfig
from pydantic import Field

class Config(BaseConfig):
    db_url: str = Field('mysql+mysqldb://root:1@localhost/rat', allow_mutation=False)

config = Config()