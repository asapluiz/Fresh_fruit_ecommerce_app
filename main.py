from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from adapter.input.web import order_taking_controller
from adapter.out.persistance.db_config import  connect_to_mongo, close_mongo_connection

logger = logging.getLogger(__name__)


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


@app.exception_handler(Exception) 
def unexpected_error(request, exc):
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )
