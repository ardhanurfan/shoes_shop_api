import uvicorn
from fastapi import FastAPI

from routes.brand import brand
from routes.shoes import shoes
from routes.varian import varian
from routes.auth import auth

app = FastAPI()

app.include_router(brand)
app.include_router(shoes)
app.include_router(varian)
app.include_router(auth)