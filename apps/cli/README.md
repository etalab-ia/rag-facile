# RAG Facile CLI

The `rf` CLI provides utility commands for managing the RAG Facile ecosystem.

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

## Usage

```bash
# Show all available commands
rf --help

# Show help for a specific command
rf template generate --help

# Check version
rf version
```

## Commands

### `template generate`

Generates a parameterized [Moon Codegen](https://moonrepo.dev/docs/guides/codegen) template from an existing application.

```bash
rf template generate --app <app-type>
```

**Arguments:**
- `--app`: The application to use as a source for the template. Supported values:
    - `chainlit-chat`
    - `reflex-chat`

**Process:**
1. Copies the source application to `.moon/templates/<app-type>`
2. Removes development artifacts (`.venv`, `.env`, `__pycache__`, etc.)
3. Applies Tera parameterization to key files (`pyproject.toml`, `.env`, `README.md`, etc.)
4. For Reflex apps, automatically renames the main package and updates internal imports using path interpolation `[var]`
5. Generates the `template.yml` configuration

## Development

The CLI is built with [Typer](https://typer.tiangolo.com/).

For development setup and contribution guidelines, see the main [CONTRIBUTING.md](../../CONTRIBUTING.md) file.

**Source code structure:**
- `src/cli/` - Main CLI package
- `src/cli/commands/` - Command definitions
