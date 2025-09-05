from typing import Union
from mangum import Mangum
from fastapi import FastAPI
from src.routes.user import router as user_router
from src.routes.auth import router as auth_router

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


handler = Mangum(app, lifespan="off")
