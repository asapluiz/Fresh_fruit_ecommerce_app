from dataclasses import dataclass

@dataclass(frozen=True)
class OrderLine:
    product_id: str
    quantity: int
    price: float

    def total_price(self):
        return self.price * self.quantity