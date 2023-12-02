from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.brand import brand
from routes.shoes import shoes
from routes.varian import varian
from routes.auth import auth
from routes.cleaner import cleaner

app = FastAPI()

# Setelan CORS untuk menerima permintaan dari semua domain
origins = ["*"]

# Tambahkan middleware CORS ke aplikasi
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(brand)
app.include_router(shoes)
app.include_router(varian)
app.include_router(auth)
app.include_router(cleaner)