
from typing import List
from adapter.out.persistance.order_models import Order
from application.domain.orderTaking.model.types import OrderDTO


ValidationErrors = List[str]

class CreateOrderFromDTO:
    def create(self, command:OrderDTO) -> OrderDTO:
        errors:ValidationErrors = []

        if errors:
            raise ValueError(f"Validation failed: {', '.join(errors)}")
        
        return command


    def _validate_address(self):
        pass

        