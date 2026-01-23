# Introduction

Data validation for Python developers.

## The problem with Python

Python is dynamically typed. This means you can do this:

```python
age = 25
age = "twenty-five"
age = ["25", 25, None]
```

No errors. Python doesn't care.

This flexibility is great for quick scripts. But it becomes a nightmare when you're building real applications, especially when working with external data.

## When things go wrong

Imagine you're building an API that receives user data:

```python
def create_user(data):
    user_id = data["id"]
    email = data["email"]
    age = data["age"]
    
    # Later in your code...
    birth_year = 2025 - age  # What if age is "25" instead of 25?
```

Your API receives JSON from the outside world. You expect:

```json
{"id": 1, "email": "dave@example.com", "age": 25}
```

But the API sends:

```json
{"id": 1, "email": null, "age": "unknown"}
```

Your code crashes.

## The real-world impact

In any application, you're constantly working with:

- **API responses** - External services return whatever they want
- **User input** - Never trust user data
- **Configuration** - Environment variables are always strings
- **Database records** - Data can be missing or malformed

Without validation, bugs hide until production. With Pydantic, they surface immediately.

## What Pydantic does

Pydantic validates data at runtime. You define what your data should look like, and Pydantic ensures it matches:

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    email: str
    age: int

# Valid data - works fine
user = User(id=1, email="dave@example.com", age=25)

# Invalid data - fails immediately with clear error
user = User(id=1, email=None, age="unknown")
```

When validation fails, you get a clear error message telling you exactly what went wrong:

```
validation error for User
email
  Input should be a valid string
age
  Input should be a valid integer, unable to parse string as an integer
```

No more debugging mysterious runtime errors. The problem is caught at the source.

## Pydantic in the Python ecosystem

Pydantic is everywhere:

- **FastAPI** uses Pydantic for request/response validation
- **Django Ninja** uses Pydantic for API schemas
- **SQLModel** combines Pydantic with SQLAlchemy
- **Most modern Python frameworks** rely on Pydantic under the hood

Learning Pydantic is about writing reliable, type-safe Python code.

## Installation

Install Pydantic in your project with either `pip` or `uv`:

```bash
pip install pydantic
```

```bash
uv add pydantic
```

## Your first model

Here's a taste of what you'll build. A simple model for an API configuration:

```python
from pydantic import BaseModel

class APIConfig(BaseModel):
    api_key: str
    model: str = "gpt-4"
    max_tokens: int = 1000
    temperature: float = 0.7

# Create a config
config = APIConfig(api_key="sk-abc123")

print(config.model)        # gpt-4
print(config.max_tokens)   # 1000
print(config.api_key)      # sk-abc123
```

Notice how:
- `api_key` is required (no default value)
- `model`, `max_tokens`, and `temperature` have defaults
- Everything is typed and validated

## Learn more

- [Official Pydantic documentation](https://docs.pydantic.dev/latest/)
- [Pydantic on GitHub](https://github.com/pydantic/pydantic)

## What's next?

Before diving deeper into Pydantic, you need to understand type hints. They're the foundation Pydantic builds on.

[Next: Type Hints](02-type-hints.md)
