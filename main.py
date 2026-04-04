from contextlib import asynccontextmanager
from fastapi import FastAPI
from adapter.input.web import order_taking_controller
from adapter.out.persistance.db_config import  connect_to_mongo, close_mongo_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    
    yield
    await close_mongo_connection()


app = FastAPI(lifespan=lifespan)

app.include_router(router=order_taking_controller.router, prefix='/api/orders', tags=['create_Orders'])

@app.get("/")
def read_root() -> dict[str, str]:

    return {"Hello": "World"}
