from adapter.out.persistance.order_models import Order as DBOrder, OrderItem as DBOrderItem
from application.domain.orderTaking.model.order import Order as DomainOrder, OrderStatus
from application.domain.orderTaking.model.orderItem import OrderLine
from application.domain.orderTaking.model.value_objects import Address, Money, OrderQuantity
from application.domain.orderTaking.model.types import OrderDTO, OrderLineDTO


class OrderMapper:
    @staticmethod
    def to_persistence(domain_order: DomainOrder) -> DBOrder:

        db_items = [
            DBOrderItem(
                product_id=line.product_id,
                quantity=line.quantity.value,
                price=line.price.amount,
            )
            for line in domain_order.order_lines
        ]
        
        return DBOrder(
            billing_address=domain_order.billing_address.value,
            delivery_address=domain_order.delivery_address.value,
            order_status=domain_order.order_status.value,
            items=db_items
        )
    
    @staticmethod
    def to_domain(db_order: DBOrder) -> DomainOrder:
        # Convert DB items to OrderLineDTO objects (with primitives)
        order_lines_dto = [
            OrderLineDTO(
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price,
            )
            for item in db_order.items
        ]
        
        # Create OrderDTO for the domain Order.create() method
        order_dto = OrderDTO(
            order_id=str(db_order.id),
            billing_address=db_order.billing_address,
            delivery_address=db_order.delivery_address,
            customer_id="testing",  # TODO: fix this field - DB model doesn't store customer_id
            order_lines=order_lines_dto
        )
        
        # Use the create method to construct and validate the domain order
        domain_order = DomainOrder.create(order_dto)
        
        # Restore the order status from database
        domain_order.order_status = OrderStatus(db_order.order_status)
        return domain_order
