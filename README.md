# RAG Facile

> [!IMPORTANT]
> This project is a starter kit for RAG applications in the French government.

## Overview

RAG Facile provides a foundation for building RAG (Retrieval-Augmented Generation) applications in the French government, specifically using the [Albert API](https://albert.sites.beta.gouv.fr/). It is designed for exploratory greenfield projects.

## Installation

### Prerequisites

Ensure you have `uv` installed on your system:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with Homebrew
brew install uv

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Install the CLI

Install the RAG Facile CLI (`rf`) globally using `uv`:

```bash
uv tool install rf --from git+https://github.com/etalab-ia/rag-facile.git#subdirectory=apps/cli
```

Verify the installation:

```bash
rf version
```

To upgrade to the latest version:

```bash
uv tool install rf --force --from git+https://github.com/etalab-ia/rag-facile.git#subdirectory=apps/cli
```

## Usage

The `rf` CLI provides commands for managing RAG applications:

```bash
# Show available commands
rf --help

# Generate a template
rf template generate --app chainlit-chat

# Check version
rf version
```

## Components

RAG Facile provides application templates for building RAG applications:

### Currently Available

- **ChainLit Chat**: A chat interface built with ChainLit
- **Reflex Chat**: Interactive chat built with Reflex

### Planned Templates

- **Admin UI**: Administration interface (coming soon)
- **Ingestion Pipeline**: Data processing pipeline (coming soon)

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and contribution guidelines.

## License

See [LICENSE](LICENSE) for details.
