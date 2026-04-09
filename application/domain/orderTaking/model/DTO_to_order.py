
from typing import List, Union
from application.domain.orderTaking.model.types import OrderDTO, OrderLineDTO
from application.domain.orderTaking.model.orderItem import OrderLine
from application.domain.orderTaking.model.value_objects import Address, Money, OrderQuantity


ValidationErrors = List[str]

class CreateOrderFromDTO:
    def __init__(self):
        self.errors: ValidationErrors = []

    def create(self, command: OrderDTO) -> dict:
        """Validate and convert DTO - returns dict of converted values for Order creation"""
        self.errors = []
        converted_lines = self._convert_order_lines(command.order_lines)
        converted_billing = self._convert_address(command.billing_address, "billing_address")
        converted_delivery = self._convert_address(command.delivery_address, "delivery_address")

        if self.errors:
            raise ValueError(f"Validation failed: {', '.join(self.errors)}")
        
        return {
            "order_id": command.order_id,
            "billing_address": converted_billing,
            "delivery_address": converted_delivery,
            "customer_id": command.customer_id,
            "order_lines": converted_lines
        }

    def _convert_order_lines(self, order_lines: List[OrderLineDTO]) -> List[OrderLine]:
        """Convert OrderLineDTO (primitives) to OrderLine (value objects)"""
        converted_lines = []
        
        # Constraint 1: Must have at least 1 order line
        if not order_lines or len(order_lines) == 0:
            self.errors.append("Order must have at least 1 order line")
            return converted_lines
        
        # Convert each order line
        for index, line in enumerate(order_lines):
            converted_line = self._convert_order_line(line, index)
            if converted_line:
                converted_lines.append(converted_line)
        
        return converted_lines

    def _convert_order_line(self, line: OrderLineDTO, index: int) -> OrderLine | None:
        """Convert OrderLineDTO to OrderLine with value objects"""
        # Validate product_id
        if not line.product_id or len(line.product_id.strip()) == 0:
            self.errors.append(f"Order line {index + 1}: product_id cannot be empty")
            return
        
        try:
            quantity = OrderQuantity(line.quantity)
        except ValueError as e:
            self.errors.append(f"Order line {index + 1}: quantity - {str(e)}")
            return
        
        # Convert price (float) to Money value object
        try:
            price = Money(line.price)
        except ValueError as e:
            self.errors.append(f"Order line {index + 1}: price - {str(e)}")
            return
        
        # Only create OrderLine if all conversions succeeded
        return OrderLine(
            product_id=line.product_id,
            quantity=quantity,
            price=price
        )

    def _convert_address(self, address: str, field_name: str) -> Address | None:
        """Convert string to Address value object"""
        try:
            return Address(address)
        except ValueError as e:
            self.errors.append(f"{field_name}: {str(e)}")


        