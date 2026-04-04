
from enum import Enum

from application.domain.orderTaking.model.DTO_to_order import CreateOrderFromDTO, ValidationErrors
from application.domain.orderTaking.model.types import OrderDTO

class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    BILLED = "billed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    

class Order:
    def __init__(self, order_DTO: OrderDTO):
        self.id = order_DTO.order_id
        self.billing_address = order_DTO.billing_address
        self.delivery_address =  order_DTO.delivery_address
        self.customer_id = order_DTO.customer_id
        self.order_status = OrderStatus.PENDING
        self.order_lines = order_DTO.order_lines

    @classmethod
    def create(cls, order_DTO:OrderDTO):
        dto_to_order = CreateOrderFromDTO()
        validated_order_dto = dto_to_order.create(order_DTO)
        return cls(validated_order_dto)
        

    def cancel(self) -> None:
        if self.order_status in [OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
            raise ValueError("Cannot cancel shipped/delivered orders")
        self.order_status = OrderStatus.CANCELLED

    def confirmed(self) -> None:
        if self.order_status != OrderStatus.PENDING:
            raise ValueError("Only pending orders can be confirmed")
        self.order_status = OrderStatus.CONFIRMED

    