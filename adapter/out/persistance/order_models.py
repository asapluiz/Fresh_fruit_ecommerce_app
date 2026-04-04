
from datetime import datetime, timezone
from typing import List

from beanie import Document
from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price: float

class Order(Document):
    billing_address: str
    delivery_address: str
    order_status: str
    items: List[OrderItem]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Settings:
        name = "orders"

class User(Document):
    name: str
    date_of_birth: datetime
    address: str
    
    class Settings:
        name = "users"