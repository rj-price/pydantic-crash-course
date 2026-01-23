# Structured LLM Output

Get type-safe responses from AI models

## The problem with LLM responses

Large language models return text. Just text:

```python
response = "The product is a laptop. It costs $999. The brand is Apple."
```

But you need structured data:

```python
{
    "product": "laptop",
    "price": 999,
    "brand": "Apple"
}
```

You could parse the text manually. But that's fragile. The model might format things differently next time.

## Structured outputs

Modern LLM APIs support structured outputs. You define a schema, and the model returns data matching that schema. Pydantic is perfect for this.

## OpenAI with Pydantic

OpenAI's API directly supports Pydantic models for structured output:

```python
from openai import OpenAI
from pydantic import BaseModel

class ProductInfo(BaseModel):
    name: str
    price: float
    category: str
    in_stock: bool

client = OpenAI()

response = client.responses.parse(
    model="gpt-4o",
    input="Extract: The new MacBook Pro costs $1999 and is available now in Electronics.",
    text_format=ProductInfo
)

product = response.output_parsed
print(product.name)      # MacBook Pro
print(product.price)     # 1999.0
print(product.category)  # Electronics
print(product.in_stock)  # True
```

The response is automatically parsed into your Pydantic model.

## Defining extraction schemas

Create models that match what you want to extract:

```python
from pydantic import BaseModel, Field

class ContactInfo(BaseModel):
    name: str = Field(description="Full name of the person")
    email: str | None = Field(description="Email address if mentioned")
    phone: str | None = Field(description="Phone number if mentioned")
    company: str | None = Field(description="Company name if mentioned")
```

Descriptions help the LLM understand what to extract.

## Complex extractions

Handle nested and list data:

```python
from pydantic import BaseModel, Field

class ActionItem(BaseModel):
    task: str
    assignee: str | None = None
    due_date: str | None = None

class MeetingNotes(BaseModel):
    title: str
    date: str
    attendees: list[str]
    summary: str
    action_items: list[ActionItem]
    next_meeting: str | None = None

# Use with OpenAI
client = OpenAI()

response = client.responses.parse(
    model="gpt-4o",
    input="""
    Meeting: Q1 Planning
    Date: January 15, 2025
    Attendees: Alice, Bob, Charlie
    
    We discussed the roadmap. Alice will prepare the budget by Friday.
    Bob is handling the technical specs. Next sync on January 22.
    """,
    text_format=MeetingNotes
)

notes = response.output_parsed
print(f"Meeting: {notes.title}")
print(f"Attendees: {', '.join(notes.attendees)}")
for item in notes.action_items:
    print(f"  - {item.task} ({item.assignee})")
```

## Handling validation errors

LLMs can sometimes return unexpected data. Handle validation gracefully:

```python
from openai import OpenAI
from pydantic import BaseModel, ValidationError

class Product(BaseModel):
    name: str
    price: float
    category: str

client = OpenAI()

try:
    response = client.responses.parse(
        model="gpt-4o",
        input="Extract product info from: Check out our new widget!",
        text_format=Product
    )
    product = response.output_parsed
    print(f"Got: {product.name}")
except ValidationError as e:
    print("Could not parse response:")
    for error in e.errors():
        print(f"  - {error['loc']}: {error['msg']}")
```

## Retry with validation feedback

Pydantic's human-readable errors make retries effective:

```python
from openai import OpenAI
from pydantic import BaseModel, ValidationError, Field

class Product(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt=0)
    category: str

def extract_product(text: str, max_retries: int = 3) -> Product | None:
    client = OpenAI()
    
    for attempt in range(max_retries):
        try:
            response = client.responses.parse(
                model="gpt-4o",
                input=f"Extract product info: {text}",
                text_format=Product
            )
            return response.output_parsed
        except ValidationError as e:
            if attempt < max_retries - 1:
                # Include error in next attempt
                error_msg = str(e)
                text = f"{text}\n\nPrevious attempt failed: {error_msg}\nPlease fix these issues."
            else:
                return None
    
    return None

# Usage
product = extract_product("New laptop, $999, Electronics")
if product:
    print(f"Extracted: {product.name}")
else:
    print("Failed to extract product info")
```

The human-readable error messages help the model understand what went wrong.

## Using Literal for constrained outputs

Force the model to choose from specific values:

```python
from typing import Literal
from pydantic import BaseModel

class SentimentAnalysis(BaseModel):
    text: str
    sentiment: Literal["positive", "negative", "neutral"]
    confidence: float

class Classification(BaseModel):
    text: str
    category: Literal["bug", "feature", "question", "other"]
    priority: Literal["low", "medium", "high"]
```

The model can only return values from your defined options.

## Real-world example: Invoice extraction

Extract structured data from unstructured invoice text:

```python
from pydantic import BaseModel, Field
from typing import Literal

class LineItem(BaseModel):
    description: str
    quantity: int = Field(ge=1)
    unit_price: float = Field(ge=0)
    
    @property
    def total(self) -> float:
        return self.quantity * self.unit_price

class Invoice(BaseModel):
    invoice_number: str
    date: str
    vendor_name: str
    vendor_address: str | None = None
    items: list[LineItem]
    subtotal: float
    tax: float | None = None
    total: float
    payment_status: Literal["paid", "pending", "overdue"] = "pending"

# Extract from invoice text
invoice_text = """
Invoice #INV-2025-001
Date: January 15, 2025
From: Acme Corp, 123 Business St

Items:
- Widget Pro (5) @ $29.99 each
- Service Fee (1) @ $50.00

Subtotal: $199.95
Tax: $16.00
Total: $215.95

Status: Paid
"""

client = OpenAI()
response = client.responses.parse(
    model="gpt-4o",
    input=f"Extract invoice data:\n{invoice_text}",
    text_format=Invoice
)

invoice = response.output_parsed
print(f"Invoice: {invoice.invoice_number}")
print(f"From: {invoice.vendor_name}")
print(f"Total: ${invoice.total}")
print(f"Status: {invoice.payment_status}")
```

## Without OpenAI's parsing

If using other LLM providers, request JSON and validate manually:

```python
import json
from pydantic import BaseModel, ValidationError

class Product(BaseModel):
    name: str
    price: float

# Assume you got this JSON string from any LLM
llm_response = '{"name": "Widget", "price": 29.99}'

try:
    data = json.loads(llm_response)
    product = Product.model_validate(data)
    print(f"Valid: {product.name}")
except json.JSONDecodeError:
    print("Invalid JSON from LLM")
except ValidationError as e:
    print(f"Validation failed: {e}")
```

## Why Pydantic for AI?

Pydantic makes AI applications reliable:

1. **Schema definition** - Clear, typed data structures
2. **Automatic validation** - Catch errors immediately
3. **Human-readable errors** - Useful for debugging and retries
4. **IDE support** - Autocomplete and type checking
5. **Ecosystem integration** - Works with FastAPI, LangChain, and more

## Summary

You've learned the complete Pydantic workflow for AI development:

1. **Type hints** - Define what data should look like
2. **BaseModel** - Create validated data structures
3. **Field constraints** - Control acceptable values
4. **Nested models** - Handle complex data
5. **Settings** - Manage configuration safely
6. **Structured output** - Get reliable data from LLMs

Pydantic is the foundation of type-safe Python for AI. Use it everywhere.

[Back to course overview](../index.md)
