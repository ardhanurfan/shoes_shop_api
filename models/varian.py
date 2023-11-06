from pydantic import BaseModel

class Varian(BaseModel):
    shoes_id:int
    color:str
    virtual_url:str
