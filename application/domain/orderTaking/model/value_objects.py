class OrderQuantity:
    """Value object representing an order quantity with domain constraints"""
    MAX_QUANTITY = 100
    MIN_QUANTITY = 1
    
    def __init__(self, value: int):
        if not isinstance(value, int):
            raise ValueError("Quantity must be an integer")
        if value < self.MIN_QUANTITY:
            raise ValueError(f"Quantity must be at least {self.MIN_QUANTITY}")
        if value > self.MAX_QUANTITY:
            raise ValueError(f"Quantity cannot exceed {self.MAX_QUANTITY}")
        self._value = value
    
    @property
    def value(self) -> int:
        return self._value
    
    def __eq__(self, other):
        if isinstance(other, OrderQuantity):
            return self._value == other._value
        return False
    
    def __hash__(self):
        return hash(self._value)
    
    def __repr__(self):
        return f"OrderQuantity({self._value})"
    
    
class Money:
    """Value object for amounts to bill"""
    def __init__(self, amount: float, currency: str = "USD"):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        self._amount = amount
        self._currency = currency
    
    @property
    def amount(self) -> float:
        return self._amount
    
    @property
    def currency(self) -> str:
        return self._currency
    
    def __eq__(self, other):
        if isinstance(other, Money):
            return self._amount == other._amount and self._currency == other._currency
        return False
    
    def __repr__(self):
        return f"Money({self._amount} {self._currency})"


class Address:
    """Value object for delivery/billing addresses"""
    def __init__(self, address: str):
        if not address or len(address.strip()) == 0:
            raise ValueError("Address cannot be empty")
        self._address = address
    
    @property
    def value(self) -> str:
        return self._address
    
    def __eq__(self, other):
        if isinstance(other, Address):
            return self._address == other._address
        return False
    
    def __repr__(self):
        return f"Address({self._address})"