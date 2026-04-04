
from application.domain.orderTaking.model.order import Order, OrderDTO
from application.domain.orderTaking.model.orderItem import OrderLine
from application.port.incoming.interface_order_taking import IConfirmOrderUsecase
from application.port.outgoing.interface_order_repository import IOrderRepository


class ConfirmOrderUsecase(IConfirmOrderUsecase):
    
    async def execute(self, order_repository: IOrderRepository):

        items = OrderLine(
            product_id = '1',
            quantity= 2,
            price= 3.6,
        )

        test:OrderDTO = {
            "order_id": "1111",
            "customer_id": "222",
            "billing_address": "test address",
            "delivery_address": "test billing address",
            "order_lines": [items]
        }

        order = Order(test)
        order.confirmed()

        await order_repository.save(order)
    