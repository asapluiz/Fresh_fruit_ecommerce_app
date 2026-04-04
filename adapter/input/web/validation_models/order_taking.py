

from typing import List
from pydantic import BaseModel



class OrderLine(BaseModel):
    product_id: str
    quantity: int
    price: float


class CreateOrderInput(BaseModel):
    billing_address: str
    delivery_address: str
    customer_id: str
    order_lines: List[OrderLine]


class CreateOrderResponse(BaseModel):
    order_id: str
    delivery_address: str
    customer_id: str
    order_lines: List[OrderLine]