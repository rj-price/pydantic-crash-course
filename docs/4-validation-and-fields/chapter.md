# Validation and Fields

Control what data is acceptable

## Beyond type checking

Pydantic validates types, but you often need more:

- Email must be a valid format
- Age must be positive
- Username must be 3-20 characters
- Price can't be negative

The `Field()` function lets you add these constraints.

## The Field function

Import `Field` from pydantic and use it to add constraints:

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(gt=0, le=120)
    email: str

user = User(name="Alice", age=30, email="alice@example.com")
```

Now `name` must be 1-100 characters, and `age` must be between 1 and 120.

## String constraints

Control string length and format:

```python
from pydantic import BaseModel, Field

class UserProfile(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    bio: str = Field(max_length=500)
    website: str = Field(pattern=r"^https?://.*")

# Valid
profile = UserProfile(
    username="alice_dev",
    bio="Python developer",
    website="https://example.com"
)

# Invalid - username too short
profile = UserProfile(username="ab", bio="Hi", website="https://x.com")
# ValidationError: username must be at least 3 characters
```

String constraints:
- `min_length` - Minimum number of characters
- `max_length` - Maximum number of characters
- `pattern` - Regular expression pattern to match

## Numeric constraints

Control number ranges:

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str
    price: float = Field(gt=0)           # Greater than 0
    quantity: int = Field(ge=0)          # Greater than or equal to 0
    discount: float = Field(ge=0, le=1)  # Between 0 and 1

product = Product(
    name="Widget",
    price=29.99,
    quantity=100,
    discount=0.15
)
```

Numeric constraints:
- `gt` - Greater than
- `ge` - Greater than or equal to
- `lt` - Less than
- `le` - Less than or equal to

## Default values with Field

Set defaults while also adding constraints:

```python
from pydantic import BaseModel, Field

class APIConfig(BaseModel):
    api_key: str
    model: str = Field(default="gpt-4")
    max_tokens: int = Field(default=1000, ge=1, le=4096)
    temperature: float = Field(default=0.7, ge=0, le=2)

# Only api_key required
config = APIConfig(api_key="sk-abc123")

print(config.model)        # gpt-4
print(config.max_tokens)   # 1000
print(config.temperature)  # 0.7
```

## Field descriptions

Add descriptions for documentation:

```python
from pydantic import BaseModel, Field

class Order(BaseModel):
    order_id: str = Field(description="Unique order identifier")
    total: float = Field(gt=0, description="Order total in USD")
    items: int = Field(ge=1, description="Number of items in order")
```

Descriptions appear in generated JSON schemas and API documentation.

## Understanding validation errors

Pydantic gives you detailed, human-readable errors:

```python
from pydantic import BaseModel, Field, ValidationError

class User(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(ge=0, le=120)
    email: str

try:
    user = User(name="A", age=-5, email=123)
except ValidationError as e:
    print(e)
```

Output:

```
3 validation errors for User
name
  String should have at least 2 characters [type=string_too_short]
age
  Input should be greater than or equal to 0 [type=greater_than_equal]
email
  Input should be a valid string [type=string_type]
```

Each error tells you:
- Which field failed
- What went wrong
- The validation type

## Accessing error details

You can access error details programmatically:

```python
from pydantic import BaseModel, Field, ValidationError

class User(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(ge=0)

try:
    user = User(name="A", age=-5)
except ValidationError as e:
    for error in e.errors():
        print(f"Field: {error['loc'][0]}")
        print(f"Message: {error['msg']}")
        print(f"Type: {error['type']}")
        print("---")
```

Output:

```
Field: name
Message: String should have at least 2 characters
Type: string_too_short
---
Field: age
Message: Input should be greater than or equal to 0
Type: greater_than_equal
---
```

## Custom validators (80/20 overview)

Sometimes built-in constraints aren't enough. Pydantic supports custom validators:

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    email: str
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v.lower()  # Normalize to lowercase

user = User(email="ALICE@Example.com")
print(user.email)  # alice@example.com
```

Custom validators let you:
- Add complex validation logic
- Transform values (like normalizing email to lowercase)
- Validate based on business rules

For most cases, built-in constraints are enough. Use custom validators when you need specific business logic.

## Real-world example

Here's a model for a payment form:

```python
from pydantic import BaseModel, Field

class PaymentForm(BaseModel):
    card_number: str = Field(min_length=16, max_length=16)
    expiry_month: int = Field(ge=1, le=12)
    expiry_year: int = Field(ge=2024)
    cvv: str = Field(min_length=3, max_length=4)
    amount: float = Field(gt=0, description="Amount in USD")
    currency: str = Field(default="USD", min_length=3, max_length=3)

payment = PaymentForm(
    card_number="1234567890123456",
    expiry_month=12,
    expiry_year=2025,
    cvv="123",
    amount=99.99
)
```

## Common patterns

### Email validation

```python
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr  # Built-in email validation

# Install email-validator: pip install email-validator
```

### URL validation

```python
from pydantic import BaseModel, HttpUrl

class Link(BaseModel):
    url: HttpUrl  # Must be valid HTTP/HTTPS URL
```

### Constrained lists

```python
from pydantic import BaseModel, Field

class Order(BaseModel):
    items: list[str] = Field(min_length=1)  # At least one item
```

## What's next?

You know how to validate individual fields. Next, let's learn how to handle complex data with nested models.

[Next: Nested Models](../5-nested-models/chapter.md)
