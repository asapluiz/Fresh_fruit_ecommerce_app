from dataclasses import dataclass

from application.domain.orderTaking.model.value_objects import Money, OrderQuantity

@dataclass(frozen=True)
class OrderLine:
    product_id: str
    quantity: OrderQuantity
    price: Money
