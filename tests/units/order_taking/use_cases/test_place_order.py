
from unittest.mock import Mock
import pytest

from application.domain.orderTaking.model.orderItem import OrderLine
from application.domain.orderTaking.services.create_order_usecase import PlaceOrderUsecase
from application.port.incoming.interface_order_taking import CreateOrderDTO, CreateOrderResponseDTO

class OrderItem1:
    product_id = "12178370-65f8-4649-88fc-b4cbe43a8706"
    quantity = 2
    price = 300

class OrderItem2:
    product_id = "7e0ac5c1-22a5-4564-965c-0318a287b7f9"
    quantity = 10
    price = 100


class TestPlaceOrder:
    def test_place_order(self):    
        order_lines = [
            OrderLine(product_id=OrderItem1.product_id, quantity=OrderItem1.quantity, price=OrderItem1.price),
            OrderLine(product_id=OrderItem2.product_id, quantity=OrderItem2.quantity, price=OrderItem2.price)
        ]
        create_order_dto = CreateOrderDTO(
            billing_address="Joseph-haydn-str 30",
            delivery_address="Joseph-haydn-str 30",
            customer_id="5aa2a107-12be-4d11-988b-46d892ef0c28",
            order_lines=order_lines
        )

        created_order = CreateOrderResponseDTO(
            order_id="test_id",
            delivery_address="Joseph-haydn-str 30",
            customer_id="5aa2a107-12be-4d11-988b-46d892ef0c28",
            order_lines=order_lines
        )

        place_order_usecase = PlaceOrderUsecase()
        mock_order_repository = Mock()
        new_order = place_order_usecase.execute(create_order_dto, mock_order_repository )
        assert(new_order.delivery_address == created_order.delivery_address)
        assert(new_order.customer_id == created_order.customer_id)
        assert(new_order.order_lines == created_order.order_lines)
        assert(new_order.order_id)