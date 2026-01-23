# Pydantic Crash Course

Type-safe Python for AI development.

## What you'll learn

Learn Pydantic from scratch and start building type-safe Python applications. This crash course covers the essential 80/20 of Pydantic with a focus on AI development.

- **Understand the problem** - Why Python's dynamic typing breaks things
- **Type hints** - The foundation Pydantic builds on
- **Data models** - Define and validate your data structures
- **Configuration** - Type-safe settings from environment variables
- **AI integration** - Get structured output from LLMs

## Course chapters

| Chapter | Topic | Description |
|---------|-------|-------------|
| 1 | [Introduction](docs/1-introduction/chapter.md) | Why Pydantic matters |
| 2 | [Type Hints](docs/2-type-hints/chapter.md) | Python's type system basics |
| 3 | [Your First Model](docs/3-your-first-model/chapter.md) | BaseModel fundamentals |
| 4 | [Validation and Fields](docs/4-validation-and-fields/chapter.md) | Control what data is acceptable |
| 5 | [Nested Models](docs/5-nested-models/chapter.md) | Handle complex data structures |
| 6 | [Pydantic Settings](docs/6-pydantic-settings/chapter.md) | Configuration management |
| 7 | [Structured LLM Output](docs/7-structured-llm-output/chapter.md) | AI integration with OpenAI |

## Prerequisites

This course assumes you know basic Python:

- Variables and data types
- Functions and classes
- Dictionaries and lists
- Working with APIs

If you need a refresher, check out the [Python for AI course](https://python.datalumina.com).

## Getting started

1. Clone this repository
2. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install pydantic pydantic-settings openai
```

4. Start with [Chapter 1: Introduction](docs/1-introduction/chapter.md)

## Resources

- [Pydantic Documentation](https://docs.pydantic.dev)
- [Pydantic Settings Documentation](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
- [Python for AI Course](https://python.datalumina.com)
