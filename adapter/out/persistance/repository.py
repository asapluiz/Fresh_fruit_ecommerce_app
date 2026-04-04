from adapter.out.persistance.order_mapper import OrderMapper
from application.port.outgoing.interface_order_repository import IOrderRepository
from application.domain.orderTaking.model.order import Order as DomainOrder


class Repository(IOrderRepository):
    async def save(self, order: DomainOrder) -> None:
        persistence_order = OrderMapper.to_persistence(order)
        await persistence_order.insert()