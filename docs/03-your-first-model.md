# Your First Model

Create validated data structures with BaseModel

## What is a model?

A Pydantic model is a class that defines the structure of your data. It specifies what fields exist and what types they should be:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int
```

This model says: "A User has a name (string), email (string), and age (integer)."

## Dataclasses vs Pydantic

Python has built-in dataclasses for defining data structures:

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str
    age: int

user = User(name="Alice", email="alice@example.com", age="not a number")
print(user.age)  # "not a number" - no validation!
```

Dataclasses give you a clean syntax for data containers, but they don't validate anything. The type hints are just documentation.

Pydantic models look similar but actually enforce the types:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int

user = User(name="Alice", email="alice@example.com", age="not a number")
# ValidationError: Input should be a valid integer
```

Use dataclasses when you trust your data (internal code, already validated). Use Pydantic when you need validation (external APIs, user input, configuration).

## Creating instances

Create a model instance by passing data to it:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int

# Create a user
user = User(name="Alice", email="alice@example.com", age=30)

print(user.name)   # Alice
print(user.email)  # alice@example.com
print(user.age)    # 30
```

Pydantic validates the data when you create the instance. Invalid data raises an error immediately.

## Validation in action

Try passing invalid data:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int

# This will raise a validation error
user = User(name="Alice", email="alice@example.com", age="thirty")
```

Error:

```
ValidationError: 1 validation error for User
age
  Input should be a valid integer, unable to parse string as an integer
```

The error tells you exactly what went wrong and where.

## Automatic type coercion

Pydantic is smart about type conversion. It converts compatible types automatically:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

# String "25" becomes integer 25
user = User(name="Alice", age="25")
print(user.age)        # 25
print(type(user.age))  # <class 'int'>
```

This is useful when working with form data or API responses where numbers come as strings.

## Required vs optional fields

Fields without defaults are required:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str              # Required
    email: str             # Required
    age: int | None = None # Optional (has default)

# Works - age is optional
user = User(name="Alice", email="alice@example.com")
print(user.age)  # None

# Also works - providing age
user = User(name="Bob", email="bob@example.com", age=25)
print(user.age)  # 25
```

## Default values

Set defaults for fields that usually have a common value:

```python
from pydantic import BaseModel

class APIConfig(BaseModel):
    api_key: str
    model: str = "gpt-4"
    max_tokens: int = 1000
    temperature: float = 0.7

# Only api_key is required
config = APIConfig(api_key="sk-abc123")

print(config.model)       # gpt-4
print(config.max_tokens)  # 1000
```

## Converting to a dictionary

Use `model_dump()` to convert a model to a dictionary:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int

user = User(name="Alice", email="alice@example.com", age=30)

# Convert to dict
user_dict = user.model_dump()
print(user_dict)
# {'name': 'Alice', 'email': 'alice@example.com', 'age': 30}
```

This is useful when you need to:
- Send data to an API
- Store in a database
- Serialize to JSON

## Converting to JSON

Use `model_dump_json()` to get a JSON string:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int

user = User(name="Alice", email="alice@example.com", age=30)

# Convert to JSON string
json_string = user.model_dump_json()
print(json_string)
# {"name":"Alice","email":"alice@example.com","age":30}
```

## Creating from a dictionary

Use `model_validate()` to create a model from a dictionary:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int

# Data from an API response
data = {"name": "Alice", "email": "alice@example.com", "age": 30}

# Create model from dict
user = User.model_validate(data)
print(user.name)  # Alice
```

This is the pattern you'll use most often: receiving data as a dictionary (from an API, database, or file) and validating it into a model.

## Models as type hints

Pydantic models work as type hints in your functions. This gives you IDE autocomplete and type checking:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str

def greet_user(user: User) -> str:
    return f"Hello, {user.name}!"

def load_user(data: dict) -> User:
    return User.model_validate(data)

# IDE knows 'user' is a User, autocomplete works
user = load_user({"name": "Alice", "email": "alice@example.com"})
message = greet_user(user)
print(message)  # Hello, Alice!
```

This makes your code self-documenting. When you see `user: User` in a function signature, you know exactly what data to pass.

## Real-world example

Here's a model for handling API responses:

```python
from pydantic import BaseModel

class WeatherResponse(BaseModel):
    city: str
    temperature: float
    humidity: int
    description: str

# Simulating API response
api_data = {
    "city": "Amsterdam",
    "temperature": 18.5,
    "humidity": 75,
    "description": "Partly cloudy"
}

# Validate and parse
weather = WeatherResponse.model_validate(api_data)

print(f"Weather in {weather.city}: {weather.temperature}°C")
print(f"Humidity: {weather.humidity}%")
print(f"Conditions: {weather.description}")
```

## Common mistakes

### Forgetting type hints

```python
# Wrong - no type hints
class User(BaseModel):
    name
    email

# Right - always include type hints
class User(BaseModel):
    name: str
    email: str
```

### Using mutable default values

```python
# Wrong - mutable default
class User(BaseModel):
    tags: list[str] = []  # All instances share the same list!

# Right - use default_factory
from pydantic import Field

class User(BaseModel):
    tags: list[str] = Field(default_factory=list)
```

### Accessing fields that don't exist

```python
user = User(name="Alice", email="alice@example.com")

# Wrong - typo in field name
print(user.nmae)  # AttributeError

# Right
print(user.name)
```

## Strict mode

By default, Pydantic coerces compatible types (like `"25"` to `25`). If you want to disable this and require exact types, use strict mode:

```python
from pydantic import BaseModel, ConfigDict

class StrictUser(BaseModel):
    model_config = ConfigDict(strict=True)
    
    name: str
    age: int

# This will fail - no coercion allowed
user = StrictUser(name="Alice", age="25")
# ValidationError: Input should be a valid integer
```

For most use cases, the default lax mode is what you want.

## Learn more

- [Models documentation](https://docs.pydantic.dev/latest/concepts/models/)
- [Dataclasses in Pydantic](https://docs.pydantic.dev/latest/concepts/dataclasses/)

## What's next?

Now you know how to create basic models. Next, let's learn how to add validation rules and constraints to your fields.

[Next: Validation and Fields](04-validation-and-fields.md)
