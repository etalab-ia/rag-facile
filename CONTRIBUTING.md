# Contributing to RAG Facile

Thank you for your interest in contributing to RAG Facile! This document provides information for developers and contributors who want to work on the monorepo.

## Development Setup

### Prerequisites

- **Python 3.13**
- **uv** (package manager)
- **just** (command runner)
- **git**

### 1. Clone the Repository

```bash
git clone https://github.com/etalab-ia/rag-facile.git
cd rag-facile
```

### 2. Install Dependencies

The project uses `uv` for package management. Install all dependencies:

```bash
just setup
```

This will:
- Create a Python 3.13 virtual environment
- Install all dependencies for all apps and packages
- Set up the development environment

### 3. Environment Variables

For the chat apps, copy the example environment files and add your credentials:

```bash
cp apps/reflex-chat/.env.example apps/reflex-chat/.env
cp apps/chainlit-chat/.env.example apps/chainlit-chat/.env
```

Using the Albert API requires specifying both `OPENAI_API_KEY` and `OPENAI_BASE_URL`.

## Project Structure

The project is organized as a monorepo with the following structure:

```
rag-facile/
├── apps/              # Application components
│   ├── chainlit-chat/ # ChainLit chat interface
│   ├── reflex-chat/  # Reflex chat interface
│   ├── admin/        # Admin UI (Streamlit)
│   ├── ingestion/    # Data ingestion pipeline
│   └── cli/          # Command-line interface
├── packages/         # Shared packages
│   └── sample/       # Sample package
├── .moon/templates/  # Generated project templates
├── scripts/          # Utility scripts
├── pyproject.toml    # Root workspace configuration
└── justfile         # Command recipes
```

## Tech Stack

- **Language**: Python 3.13
- **Package Manager**: `uv`
- **Monorepo Manager**: `moon`
- **Command Runner**: `just`
- **Linting**: `ruff`
- **Type Checking**: `ty`

## Development Workflow

### Running Applications

Use `just` to run any of the applications from the root directory:

```bash
just reflex-chat    # Runs at http://localhost:3000
just chainlit-chat  # Runs at http://localhost:8000
just admin          # Runs admin UI
```

### Code Quality

Run linting and type checking:

```bash
# Lint all code
just lint

# Type check all code
just type-check

# Format code
just format
```

Parameterized project templates (using [Moon Codegen](https://moonrepo.dev/docs/guides/codegen)) are generated from the living "Golden Master" apps in the `apps/` directory.

To update all templates after making changes to the source apps:

```bash
just gen-templates
```

To instantiate a new project from a template:

```bash
# Default (chainlit-chat)
just create-app

# Specific template and destination
just create-app reflex-chat my-new-project
```

The generated project will include its own `Justfile` for local development:
- `just sync`: Properly synchronizes dependencies using Python 3.13
- `just run`: Runs the application

## Testing

Run tests for the entire monorepo:

```bash
just test
```

Run tests for a specific app:

```bash
cd apps/cli
uv run pytest
```

## Pull Request Process

1. **Fork and clone** the repository
2. **Create a branch** for your changes: `git checkout -b feature/your-feature`
3. **Make your changes** following the coding conventions
4. **Run tests** and ensure they pass
5. **Commit** your changes with a clear message
6. **Push** to your fork: `git push origin feature/your-feature`
7. **Create a pull request** to the main repository

## Coding Conventions

- Follow PEP 8 style guidelines
- Use type hints for all functions
- Write docstrings for public functions and classes
- Keep functions focused and small
- Use descriptive variable names

## Getting Help

- Open an issue for bugs or feature requests
- Start a discussion for questions
- Check existing issues and discussions first

## License

By contributing to RAG Facile, you agree that your contributions will be licensed under the same license as the project.
