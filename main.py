import uvicorn
from fastapi import FastAPI

from routes.brand import brand
from routes.shoes import shoes
from routes.varian import varian

app = FastAPI()

app.include_router(brand)
app.include_router(shoes)
app.include_router(varian)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=80)