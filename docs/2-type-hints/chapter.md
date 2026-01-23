# Type Hints

The foundation Pydantic builds on

## What are type hints?

Type hints tell Python (and other developers) what type of data a variable should hold:

```python
name: str = "Dave"
age: int = 30
price: float = 19.99
is_active: bool = True
```

The `: str`, `: int`, `: float`, and `: bool` are type hints.

## Python doesn't enforce them

Here's the key thing: Python ignores type hints at runtime. They're just documentation:

```python
age: int = "not a number"  # Python allows this
```

No error. Python runs this code without complaint.

So why use them?

## Why type hints matter

Type hints give you three benefits:

1. **Documentation** - Code becomes self-explanatory
2. **IDE support** - Autocomplete, error detection, refactoring
3. **Validation tools** - Pydantic, mypy, and others use them

Without type hints:

```python
def create_user(name, email, age):
    # What types are these supposed to be?
    pass
```

With type hints:

```python
def create_user(name: str, email: str, age: int) -> dict:
    # Crystal clear
    pass
```

## Basic types

The four types you'll use constantly:

```python
# Strings - text
name: str = "Alice"
message: str = "Hello, world!"

# Integers - whole numbers
count: int = 42
user_id: int = 1001

# Floats - decimal numbers
price: float = 29.99
temperature: float = 98.6

# Booleans - true or false
is_active: bool = True
has_access: bool = False
```

## Container types

For collections of data, you specify what's inside:

```python
# List of strings
tags: list[str] = ["python", "ai", "pydantic"]

# List of integers
scores: list[int] = [85, 92, 78]

# Dictionary with string keys and integer values
age_map: dict[str, int] = {"alice": 30, "bob": 25}

# Dictionary with string keys and any values
settings: dict[str, str] = {"theme": "dark", "language": "en"}
```

## Optional values

Sometimes a value might not exist. Use `Optional` or the `|` syntax:

```python
from typing import Optional

# These mean the same thing
middle_name: Optional[str] = None
middle_name: str | None = None
```

Use `Optional` when a field might be `None`:

```python
class User:
    name: str                      # Required
    email: str                     # Required
    phone: str | None = None       # Optional, defaults to None
    bio: Optional[str] = None      # Same thing, older syntax
```

## Literal types

When a value must be one of specific options:

```python
from typing import Literal

status: Literal["draft", "published", "archived"] = "draft"

# Only these three values are valid
status = "draft"      # OK
status = "published"  # OK
status = "pending"    # Type checkers will warn about this
```

Real-world example:

```python
from typing import Literal

class Task:
    title: str
    priority: Literal["low", "medium", "high"]
    status: Literal["todo", "in_progress", "done"]
```

## Function type hints

Type hints work on function parameters and return values:

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

def calculate_total(prices: list[float], tax_rate: float) -> float:
    subtotal = sum(prices)
    return subtotal * (1 + tax_rate)

def find_user(user_id: int) -> dict | None:
    # Returns a dict if found, None if not
    pass
```

The `-> str` after the parentheses indicates the return type.

## Common type hint patterns

Here are patterns you'll see constantly in Python code:

```python
from typing import Optional, Literal

# Required string
name: str

# Optional string (can be None)
nickname: str | None = None

# String with default
country: str = "USA"

# List of items
items: list[str] = []

# Dictionary
metadata: dict[str, str] = {}

# Specific allowed values
role: Literal["admin", "user", "guest"] = "user"
```

## Type hints don't validate

Remember: Python ignores type hints. This code runs without error:

```python
age: int = "not a number"
prices: list[float] = "definitely not a list"
```

Type hints are just hints. They don't enforce anything.

This is where Pydantic comes in. Pydantic reads your type hints and actually validates data against them.

## What's next?

Now that you understand type hints, let's use them with Pydantic to create your first validated data model.

[Next: Your First Model](../3-your-first-model/chapter.md)
