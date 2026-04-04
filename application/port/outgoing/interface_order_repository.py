
from abc import ABC, abstractmethod
from application.domain.orderTaking.model.order import Order


class IOrderRepository(ABC):

    @abstractmethod
    async def save(self, order:Order) -> None:
        pass