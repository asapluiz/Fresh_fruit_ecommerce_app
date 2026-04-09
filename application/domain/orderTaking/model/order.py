from enum import Enum
from typing import List

from application.domain.orderTaking.model.DTO_to_order import CreateOrderFromDTO, ValidationErrors
from application.domain.orderTaking.model.orderItem import OrderLine
from application.domain.orderTaking.model.types import OrderDTO
from application.domain.orderTaking.model.value_objects import Address, Money

class OrderStatus(Enum):
    CONFIRMED = "confirmed"
    BILLED = "billed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    

# constrains
#1) orderline must be atleast 1 
#2) number or ordered quantity must not be over 100
#3) amount to bill must be over 0

class Order:
    def __init__(self, order_id: str, billing_address: Address, delivery_address: Address, 
                 customer_id: str, order_lines: List[OrderLine]):
        """Create Order with already-validated value objects - types are explicit!"""
        self.id: str = order_id
        self.billing_address: Address = billing_address
        self.delivery_address: Address = delivery_address
        self.customer_id: str = customer_id
        self.order_status: OrderStatus = OrderStatus.CONFIRMED
        self.order_lines: List[OrderLine] = order_lines
        self.Amount_to_bill: Money = self._calculate_total()

    @classmethod
    def create(cls, order_DTO: OrderDTO):
        """Create validated Order from DTO (validates and converts primitives to value objects)"""
        validator = CreateOrderFromDTO()
        converted = validator.create(order_DTO)
        return cls(**converted)

    def cancel(self) -> None:
        if self.order_status in [OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
            raise ValueError("Cannot cancel shipped/delivered orders")
        self.order_status = OrderStatus.CANCELLED

    def confirmed(self) -> None:
        if self.order_status != OrderStatus.CONFIRMED:
            raise ValueError("Only pending orders can be confirmed")
        self.order_status = OrderStatus.CONFIRMED


    def _calculate_total(self) -> Money:
        """Calculate total from all order lines"""
        total_amount = sum(
            line.quantity.value * line.price.amount 
            for line in self.order_lines
        )
        return Money(total_amount)

    