# RAG Facile CLI

The CLI provides utility commands for managing the RAG Facile ecosystem.

## Installation

### Option 1: Persistent Installation (Recommended)
Install globally using `uv`:

```bash
uv tool install rf --from git+https://github.com/etalab-ia/rag-facile.git#subdirectory=apps/cli
```

Then use the tool directly:

```bash
rf version
rf template generate --app chainlit-chat
```

To upgrade:

```bash
uv tool install rf --force --from git+https://github.com/etalab-ia/rag-facile.git#subdirectory=apps/cli
```

### Option 2: One-time Usage
Run directly without installing:

```bash
uvx --from git+https://github.com/etalab-ia/rag-facile.git#subdirectory=apps/cli rf [command]
```

### Option 3: As Part of Monorepo
The CLI is part of the `rag-facile` monorepo workspace:

```bash
uv sync
uv run rf [command]
```

## Usage
When installed globally, the CLI is accessible via the `rf` command:

```bash
rf [command]
```

### Commands

#### `template generate`
Generates a parameterized [Copier](https://copier.readthedocs.io/) template from an existing application in the `apps/` directory.

```bash
uv run rf template generate --app <app-type>
```

**Arguments:**
- `--app`: The application to use as a source for the template. Supported values:
    - `chainlit-chat`
    - `reflex-chat`

**Description:**
1. Copies the source application to `templates/<app-type>`.
2. Removes development artifacts (`.venv`, `.env`, `__pycache__`, etc.).
3. Applies Jinja2 parameterization to key files (`pyproject.toml`, `.env`, `README.md`, etc.).
4. For Reflex apps, automatically renames the main package and updates internal imports.
5. Generates the `copier.yml` configuration.

## Development
The CLI is built with [Typer](https://typer.tiangolo.com/).
Source code is located in `src/cli/`.
Command definitions are in `src/cli/commands/`.
Copier configurations are in `src/cli/configs/`.
