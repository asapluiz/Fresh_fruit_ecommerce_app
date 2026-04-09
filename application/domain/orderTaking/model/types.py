from dataclasses import dataclass
from typing import List
from application.domain.orderTaking.model.orderItem import OrderLine


@dataclass
class OrderLineDTO:
    product_id: str
    quantity: int
    price: float

@dataclass
class OrderDTO():
    order_id: str
    billing_address: str
    delivery_address: str
    customer_id: str
    order_lines: List[OrderLineDTO]
