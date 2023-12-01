from typing import Optional
from pydantic import BaseModel

from models.brand import Brand

class Shoes(BaseModel):
    brand_id:int
    name:str
    category:str
    stock:int
    price:int
