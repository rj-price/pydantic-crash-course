# Pydantic Crash Course

Type-safe Python for AI development

## Welcome

Learn Pydantic from scratch and start building type-safe Python applications. This crash course takes you from understanding the problem Pydantic solves to using it for structured AI outputs.

Whether you've never used type hints or you're looking to level up your data validation game, this course gives you the essential 80/20 of Pydantic.

## What you'll learn

Master the Pydantic fundamentals essential for AI development:

- **Understand the problem** - Why Python's dynamic typing breaks things
- **Type hints** - The foundation Pydantic builds on
- **Data models** - Define and validate your data structures
- **Configuration** - Type-safe settings from environment variables
- **AI integration** - Get structured output from LLMs

## Course chapters

| Chapter | Topic | Description |
|---------|-------|-------------|
| 1 | [Introduction](1-introduction/chapter.md) | The problem Pydantic solves |
| 2 | [Type Hints](2-type-hints/chapter.md) | Python's type system basics |
| 3 | [Your First Model](3-your-first-model/chapter.md) | BaseModel fundamentals |
| 4 | [Validation and Fields](4-validation-and-fields/chapter.md) | Control what data is acceptable |
| 5 | [Nested Models](5-nested-models/chapter.md) | Handle complex data structures |
| 6 | [Pydantic Settings](6-pydantic-settings/chapter.md) | Configuration management |
| 7 | [Structured LLM Output](7-structured-llm-output/chapter.md) | AI integration with OpenAI |

## Prerequisites

This course assumes you know basic Python:

- Variables and data types
- Functions and classes
- Dictionaries and lists
- Working with APIs

If you need a refresher, check out the [Python for AI course](https://python.datalumina.com).

## Getting started

This project uses [uv](https://docs.astral.sh/uv/) for package management.

Install uv (if you haven't already):

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Create environment and install dependencies:

```bash
uv sync
```

Run Python files:

```bash
uv run python main.py
```

Ready? Let's start with why Pydantic exists.

[Begin the course](1-introduction/chapter.md)
