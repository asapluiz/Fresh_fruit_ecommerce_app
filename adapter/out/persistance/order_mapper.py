from adapter.out.persistance.order_models import Order as DBOrder, OrderItem as DBOrderItem
from application.domain.orderTaking.model.order import Order as DomainOrder, OrderStatus
from application.domain.orderTaking.model.orderItem import OrderLine
from application.domain.orderTaking.model.types import OrderDTO


class OrderMapper:
    @staticmethod
    def to_persistence(domain_order: DomainOrder) -> DBOrder:

        db_items = [
            DBOrderItem(
                product_id=line.product_id,
                quantity=line.quantity,
                price=line.price,
            )
            for line in domain_order.order_lines
        ]
        
        return DBOrder(
            billing_address=domain_order.billing_address,
            delivery_address=domain_order.delivery_address,
            order_status=domain_order.order_status.value,
            items=db_items
        )
    
    @staticmethod
    def to_domain(db_order: DBOrder) -> DomainOrder:
        order_lines = [
            OrderLine(
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price,
            )
            for item in db_order.items
        ]
        
        order_dto = OrderDTO(
            order_id = str(db_order.id),
            billing_address = db_order.billing_address,
            delivery_address = db_order.delivery_address,
            #TODO: fix this field below
            customer_id = "testing",  # Note: DB model doesn't store customer_id
            order_lines = order_lines
        )
        
        domain_order = DomainOrder(order_dto)
        domain_order.order_status = OrderStatus(db_order.order_status)
        return domain_order
