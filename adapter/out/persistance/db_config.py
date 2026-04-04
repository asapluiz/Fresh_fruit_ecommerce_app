from typing import Any, Optional

from beanie import init_beanie  # type: ignore[attr-defined]
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.server_api import ServerApi

from adapter.out.persistance.order_models import Order, User

MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "fruit_database"

client: Optional[AsyncIOMotorClient[Any]] = None
database: Optional[AsyncIOMotorDatabase[Any]] = None

async def connect_to_mongo() -> None:
    global client, database
    client = AsyncIOMotorClient(MONGODB_URL, server_api=ServerApi('1'))
    database= client[DATABASE_NAME]
    await init_beanie(
        database= database, # type: ignore
        document_models= [Order, User]
    )
    
    try:
        await database.command("ping")
        print("Connected to MongoDB")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        raise

async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("Disconnected from MongoDB")