
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from application.port.outgoing.interface_order_repository import IOrderRepository
from application.domain.orderTaking.model.orderItem import OrderLine

@dataclass
class CreateOrderLineDTO:
    product_id: str
    quantity: int
    price: float
@dataclass
class CreateOrderDTO():
    billing_address: str
    delivery_address: str
    customer_id: str
    order_lines: List[CreateOrderLineDTO]

@dataclass
class CreateOrderResponseDTO():
    order_id: str
    delivery_address: str
    customer_id: str
    order_lines: List[OrderLine]

class IConfirmOrderUsecase(ABC):
    @abstractmethod
    async def execute(self, order_repository: IOrderRepository) -> None:
        pass



class IPlaceOrderUsecase(ABC):
    @abstractmethod
    async def execute(self, create_order_command:CreateOrderDTO , order_repository: IOrderRepository) -> CreateOrderResponseDTO:
        pass