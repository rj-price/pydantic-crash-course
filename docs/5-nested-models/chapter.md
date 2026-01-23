# Nested Models

Handle complex data structures

## Real data is nested

Real-world data rarely comes flat. An order has items. A user has an address. A company has employees. Pydantic handles this naturally.

## Models inside models

Use one model as a field type in another:

```python
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str

class User(BaseModel):
    name: str
    email: str
    address: Address  # Nested model

# Create with nested data
user = User(
    name="Alice",
    email="alice@example.com",
    address=Address(
        street="123 Main St",
        city="Amsterdam",
        country="Netherlands",
        postal_code="1012 AB"
    )
)

print(user.address.city)  # Amsterdam
```

## Creating from dictionaries

The real power shows when parsing nested JSON or dictionaries:

```python
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    country: str

class User(BaseModel):
    name: str
    email: str
    address: Address

# Data from an API response
data = {
    "name": "Alice",
    "email": "alice@example.com",
    "address": {
        "street": "123 Main St",
        "city": "Amsterdam",
        "country": "Netherlands"
    }
}

# Pydantic validates everything, including nested data
user = User.model_validate(data)

print(user.name)           # Alice
print(user.address.city)   # Amsterdam
```

Pydantic automatically creates the nested `Address` model from the dictionary.

## Lists of models

Handle collections of nested objects:

```python
from pydantic import BaseModel

class OrderItem(BaseModel):
    product_id: str
    name: str
    quantity: int
    price: float

class Order(BaseModel):
    order_id: str
    customer_email: str
    items: list[OrderItem]  # List of models
    
    @property
    def total(self) -> float:
        return sum(item.price * item.quantity for item in self.items)

# From API response
order_data = {
    "order_id": "ORD-001",
    "customer_email": "customer@example.com",
    "items": [
        {"product_id": "P1", "name": "Widget", "quantity": 2, "price": 29.99},
        {"product_id": "P2", "name": "Gadget", "quantity": 1, "price": 49.99}
    ]
}

order = Order.model_validate(order_data)

print(f"Order {order.order_id}")
for item in order.items:
    print(f"  - {item.name}: {item.quantity} x ${item.price}")
print(f"Total: ${order.total}")
```

Output:

```
Order ORD-001
  - Widget: 2 x $29.99
  - Gadget: 1 x $49.99
Total: $109.97
```

## Optional nested models

Make nested models optional:

```python
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    country: str

class User(BaseModel):
    name: str
    email: str
    address: Address | None = None  # Optional nested model

# Works without address
user = User(name="Alice", email="alice@example.com")
print(user.address)  # None

# Works with address
user = User(
    name="Bob",
    email="bob@example.com",
    address={"street": "456 Oak Ave", "city": "Berlin", "country": "Germany"}
)
print(user.address.city)  # Berlin
```

## Deep nesting

You can nest as deep as needed:

```python
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    country: str

class Customer(BaseModel):
    name: str
    email: str
    billing_address: Address
    shipping_address: Address | None = None

class OrderItem(BaseModel):
    product_id: str
    name: str
    quantity: int
    price: float

class Order(BaseModel):
    order_id: str
    customer: Customer
    items: list[OrderItem]
    notes: str | None = None

# Complex nested data
data = {
    "order_id": "ORD-123",
    "customer": {
        "name": "Alice Smith",
        "email": "alice@example.com",
        "billing_address": {
            "street": "123 Main St",
            "city": "Amsterdam",
            "country": "Netherlands"
        }
    },
    "items": [
        {"product_id": "SKU-001", "name": "Widget", "quantity": 3, "price": 19.99}
    ]
}

order = Order.model_validate(data)
print(order.customer.billing_address.city)  # Amsterdam
```

## Real-world example: API response

Parsing a typical API response:

```python
from pydantic import BaseModel

class Coordinates(BaseModel):
    latitude: float
    longitude: float

class CurrentWeather(BaseModel):
    temperature: float
    humidity: int
    description: str

class WeatherResponse(BaseModel):
    city: str
    coordinates: Coordinates
    current: CurrentWeather
    forecast: list[CurrentWeather] = []

# API response
api_data = {
    "city": "Paris",
    "coordinates": {"latitude": 48.85, "longitude": 2.35},
    "current": {
        "temperature": 22.5,
        "humidity": 65,
        "description": "Partly cloudy"
    },
    "forecast": [
        {"temperature": 24.0, "humidity": 60, "description": "Sunny"},
        {"temperature": 21.0, "humidity": 70, "description": "Cloudy"}
    ]
}

weather = WeatherResponse.model_validate(api_data)

print(f"Weather in {weather.city}")
print(f"Current: {weather.current.temperature}°C, {weather.current.description}")
print(f"Location: {weather.coordinates.latitude}, {weather.coordinates.longitude}")
```

## Converting nested models

When you call `model_dump()`, nested models are converted too:

```python
from pydantic import BaseModel

class Address(BaseModel):
    city: str
    country: str

class User(BaseModel):
    name: str
    address: Address

user = User(
    name="Alice",
    address=Address(city="Amsterdam", country="Netherlands")
)

# Converts everything to dict
data = user.model_dump()
print(data)
# {'name': 'Alice', 'address': {'city': 'Amsterdam', 'country': 'Netherlands'}}
```

## Common patterns

### Reusing address models

```python
class Address(BaseModel):
    street: str
    city: str
    postal_code: str
    country: str

class Company(BaseModel):
    name: str
    headquarters: Address
    billing_address: Address | None = None

class Person(BaseModel):
    name: str
    home_address: Address
    work_address: Address | None = None
```

### Self-referencing models (trees)

```python
from __future__ import annotations
from pydantic import BaseModel

class Comment(BaseModel):
    text: str
    author: str
    replies: list[Comment] = []  # Comments can have replies

comment = Comment(
    text="Great article!",
    author="Alice",
    replies=[
        Comment(text="Thanks!", author="Bob", replies=[])
    ]
)
```

## What's next?

You can now handle complex data structures. Next, let's learn how to manage application configuration with Pydantic Settings.

[Next: Pydantic Settings](../6-pydantic-settings/chapter.md)
