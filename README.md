# Fresh Fruit E-Commerce App

A clean architecture-based e-commerce application for ordering fresh fruits, built with **FastAPI**, **MongoDB**, and **Python**.

## Project Overview

This is a Proof of Concept (POC) implementing clean architecture principles from "Get Hands Dirty on Clean Architecture" by Tom Hombergs. The application handles order creation, validation, and management with explicit error handling and domain-driven design.

## Tech Stack

- **Framework**: FastAPI
- **Database**: MongoDB (with Beanie ODM)
- **Language**: Python 3.13
- **Testing**: Pytest
- **Migration**: Alembic
- **Async**: Motor (async MongoDB driver)

## Architecture

```
application/                    # Core business logic (domain)
├── domain/
│   └── orderTaking/
│       ├── model/             # Domain entities & value objects
│       │   ├── order.py
│       │   ├── value_objects.py
│       │   ├── exceptions.py   # Domain-specific errors
│       │   └── DTO_to_order.py
│       └── services/          # Use cases
│           ├── create_order_usecase.py
│           └── confirm_order_usecase.py
├── port/                      # Interfaces (abstraction)
│   ├── incoming/             # Input ports (what the app exposes)
│   │   └── interface_order_taking.py
│   └── outgoing/             # Output ports (repositories)
│       └── interface_order_repository.py
│
adapter/                        # External integrations
├── input/
│   └── web/                   # HTTP controllers
│       ├── order_taking_controller.py
│       └── validation_models/
│           └── order_taking.py
└── out/
    └── persistance/           # Database adapters
        ├── repository.py
        └── order_models.py
```

## Key Features

✅ **Clean Architecture** - Separation of concerns with domain, use cases, and adapters  
✅ **Domain-Driven Design** - Rich domain models with value objects  
✅ **Explicit Error Handling** - Domain exceptions mapped to HTTP status codes  
✅ **Async/Await** - Fully asynchronous operations  
✅ **MongoDB Integration** - Document database with async support  
✅ **Type Hints** - Full Python type annotations  

## Setup Instructions

### Prerequisites
- Python 3.13+
- MongoDB running locally (or configure connection string)
- Virtual environment support

### Installation

1. **Clone and navigate to project**
```bash
cd Fresh_fruit_ecommerce_app
```

2. **Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell
source .venv/bin/activate   # macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
pip install fastapi uvicorn
```

4. **Ensure MongoDB is running**
```bash
mongod  # Start MongoDB service
```

## Running the Application

```bash
uvicorn main:app --reload
```

The app will start on `http://localhost:8000`

**Swagger UI**: `http://localhost:8000/docs`  
**ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Create Order
```
POST /api/orders/create_order
Content-Type: application/json

{
  "billing_address": "123 Main St",
  "delivery_address": "456 Oak Ave",
  "customer_id": "cust-123",
  "order_lines": [
    {
      "product_id": "prod-001",
      "quantity": 5,
      "price": 29.99
    }
  ]
}
```

**Success Response (200)**
```json
{
  "order_id": "550e8400-e29b-41d4-a716-446655440000",
  "delivery_address": "456 Oak Ave",
  "customer_id": "cust-123",
  "order_lines": [...]
}
```

**Validation Error Response (400)**
```json
{
  "error": "Validation failed: Quantity cannot exceed 100"
}
```

## Error Handling Strategy

### Domain Exceptions (Application Layer)
- `OrderError` - Base exception for all order errors
- `OrderValidationError` - Invalid inputs (quantity, price, address)
- `InvalidOrderStateError` - Invalid state transitions (e.g., cancel shipped order)
- `OrderNotFoundError` - Order doesn't exist

### HTTP Status Mapping
| Exception | HTTP Status | Meaning |
|---|---|---|
| `OrderValidationError` | 400 | Bad Request - Client sent invalid data |
| `InvalidOrderStateError` | 409 | Conflict - State violation |
| `OrderNotFoundError` | 404 | Not Found - Resource doesn't exist |
| Unexpected errors | 500 | Internal Server Error |

### Error Flow
```
Domain Layer (raises OrderError)
         ↓
Repository (converts DB errors to OrderError)
         ↓
Use Case (propagates OrderError)
         ↓
Controller (catches OrderError, maps to HTTP)
         ↓
Global Exception Handler (fallback for unexpected errors)
```

## Domain Constraints

Orders must satisfy these business rules:

1. **Order Lines**: Minimum 1 order line required
2. **Quantity**: Between 1-100 items per line
3. **Price**: Must be greater than 0
4. **Address**: Cannot be empty
5. **Order State**: Cannot cancel shipped/delivered orders

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/units/order_taking/use_cases/test_place_order.py

# With verbose output
pytest -v
```

## Logging

Logs are saved to `logs/app.log` with rotation:
- Maximum 10MB per file
- Keeps 5 backup files
- Also prints to console

## Project Structure Details

### Domain Layer (`application/domain/`)
- **Value Objects**: `Money`, `Address`, `OrderQuantity` - encapsulate domain constraints
- **Entities**: `Order`, `OrderLine` - aggregate root with business logic
- **Use Cases**: Services handling user workflows (create order, confirm order)
- **Exceptions**: Domain-specific error types

### Adapter Layer (`adapter/`)
- **Input**: HTTP controllers that handle requests
- **Output**: Repository implementations for data persistence
- Maps between HTTP and domain models

### Port Layer (`application/port/`)
- **Incoming Ports**: Interfaces defining what the app exposes
- **Outgoing Ports**: Interfaces for external dependencies (database)
- Enables pluggable implementations

## Development Notes

### Adding New Features
1. Define domain logic in `application/domain/`
2. Create use case services
3. Implement HTTP controller in `adapter/input/web/`
4. Implement repository in `adapter/out/persistance/`
5. Write tests first (TDD approach recommended)

### Import Order
```python
# Correct dependency flow:
# Adapter → Port/Interface → Domain/Use Case → Domain/Model
from application.domain.orderTaking.model.order import Order  ✅
from adapter.input.web import controller                       ✅
from adapter.out.persistance import repository                ✅

# Avoid (creates circular dependency):
from adapter.input.web import controller  # in domain model   ❌
```

## MongoDB Configuration

Connection string: `mongodb://localhost:27017`  
Database: `fruit_database`

Collections:
- `orders` - Order documents
- `users` - User information

## Next Steps

- [ ] Implement authentication/authorization
- [ ] Add billing domain
- [ ] Create order tracking/status endpoints
- [ ] Add payment integration
- [ ] Implement inventory management
- [ ] Add comprehensive API documentation

## License

POC - Learning project

## References

- [Get Hands Dirty on Clean Architecture](https://reflectoring.io/book/)
- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB with Beanie](https://beanie-odm.readthedocs.io/)
