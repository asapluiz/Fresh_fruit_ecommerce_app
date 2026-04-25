class OrderError(Exception):
    """Base exception for all order domain errors"""
    pass


# class OrderValidationError(OrderError):
#     """Raised when order data fails validation (invalid inputs)"""
#     pass


# class InvalidOrderStateError(OrderError):
#     """Raised when order state transition violates business rules"""
#     pass


# class OrderNotFoundError(OrderError):
#     """Raised when order doesn't exist"""
#     pass
