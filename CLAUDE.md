# Claude Instructions

This is a **crash course documentation repository**, not a codebase. The markdown files in `docs/` are educational content for a Pydantic tutorial video series.

## What this is

- Written documentation that accompanies a YouTube crash course
- 7 chapters teaching Pydantic from basics to AI integration
- Target audience: Python developers who know basics but haven't used type hints or data models
- Focus: 80/20 principle (teach what's used 80% of the time)

## Writing style

Follow the style from [python.datalumina.com](https://python.datalumina.com):

**Do:**
- Short, direct sentences
- Real-world examples (API configs, users, orders)
- Isolated code blocks focused on one concept
- "Common mistakes" sections
- Clear navigation between chapters

**Don't:**
- Em dashes (use commas or periods instead)
- "Why X matters" or "Why X for Y" headings (AI pattern)
- "It's worth noting", "Let's dive in", "Here's the thing"
- Generic examples (cats, dogs, foo, bar)
- Long paragraphs

## Structure

```
docs/
  index.md                    # Course overview
  1-introduction/chapter.md   # Problem and installation
  2-type-hints/chapter.md     # Type hints foundation
  3-your-first-model/         # BaseModel basics
  4-validation-and-fields/    # Field constraints
  5-nested-models/            # Complex data
  6-pydantic-settings/        # Environment variables
  7-structured-llm-output/    # AI integration
```

## Commands

```bash
uv sync          # Install dependencies
uv run python main.py  # Run example
```
