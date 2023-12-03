from pydantic import BaseModel


class User(BaseModel):
    fullname: str
    username: str
    email: str
    password: str
    cleaning_token:str