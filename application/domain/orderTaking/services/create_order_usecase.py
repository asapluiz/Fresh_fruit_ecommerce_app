
import uuid
from application.domain.orderTaking.model.order import Order
from application.domain.orderTaking.model.types import OrderDTO, OrderLineDTO
from application.port.incoming.interface_order_taking import CreateOrderDTO, CreateOrderResponseDTO, IPlaceOrderUsecase
from application.port.outgoing.interface_order_repository import IOrderRepository


class PlaceOrderUsecase(IPlaceOrderUsecase):

    
    async def execute(self,  create_order_command:CreateOrderDTO , order_repository: IOrderRepository) -> CreateOrderResponseDTO:
        order_id = str(uuid.uuid4())
        
        order_dto = OrderDTO(
            order_id=order_id,
            billing_address=create_order_command.billing_address,
            delivery_address=create_order_command.delivery_address,
            customer_id=create_order_command.customer_id,
            order_lines=[
                OrderLineDTO(
                    product_id=line.product_id,
                    quantity=line.quantity,
                    price=line.price
                )
                for line in create_order_command.order_lines
            ]
        )
        
        new_order = Order.create(order_dto)
        await order_repository.save(new_order)
        
        return CreateOrderResponseDTO(
            order_id=new_order.id,
            delivery_address=new_order.delivery_address.value,
            customer_id=new_order.customer_id,
            order_lines=new_order.order_lines
        )