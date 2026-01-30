# RAG Facile
 > [!IMPORTANT]
 > This project is a starter kit for RAG applications in the French government.

## Overview
This starter kit provides a foundation for building RAG (Retrieval-Augmented Generation) applications in the French government, specifically using the [Albert API](https://albert.sites.beta.gouv.fr/). It is designed for exploratory greenfield projects.

## Components
The project is organized as a monorepo with the following foundational components:
- **Chat Interface**: Built with ChainLit (`apps/chainlit-chat`).
- **Reflex Chat**: Interactive chat built with Reflex (`apps/reflex-chat`).
- **Admin UI**: Administration interface (`apps/admin`).
- **Ingestion Pipeline**: Data processing pipeline (`apps/ingestion`).
- **CLI**: Command-line interface (`apps/cli`).

## Tech Stack
- **Language**: Python 3.13
- **Package Manager**: `uv`
- **Monorepo Manager**: `moon`
- **Command Runner**: `just`
- **Linting**: `ruff`
- **Type Checking**: `ty`

## Getting Started

### 1. Prerequisite
Ensure you have `uv` and `just` installed on your system.

### 2. Install the CLI (Optional)
You can install the RAG Facile CLI (`rf`) globally using `uv`:

#### Option 1: Persistent Installation (Recommended)
Install once and use everywhere:
```bash
uv tool install rf --from git+https://github.com/etalab-ia/rag-facile.git#subdirectory=apps/cli
```

Then use the tool directly:
```bash
rf version
rf template generate --app chainlit-chat
```

To upgrade the CLI:
```bash
uv tool install rf --force --from git+https://github.com/etalab-ia/rag-facile.git#subdirectory=apps/cli
```

#### Option 2: One-time Usage
Run directly without installing:
```bash
uvx --from git+https://github.com/etalab-ia/rag-facile.git#subdirectory=apps/cli rf version
```

**Benefits of persistent installation:**
- Tool stays installed and available in PATH
- No need to create shell aliases
- Better tool management with `uv tool list`, `uv tool upgrade`, `uv tool uninstall`

### 3. Setup
Install all dependencies and prepare the workspace:
```bash
just setup
```

### 3. Environment Variables
For the chat apps, copy the example environment files and add your credentials. Using the Albert API requires specifying both `OPENAI_API_KEY` and `OPENAI_BASE_URL`:
```bash
cp apps/reflex-chat/.env.example apps/reflex-chat/.env
cp apps/chainlit-chat/.env.example apps/chainlit-chat/.env
```

### 4. Running the Applications
Use `just` to run any of the applications from the root directory:
- `just reflex-chat`: Runs the Reflex chat app at http://localhost:3000
- `just chainlit-chat`: Runs the ChainLit chat app at http://localhost:8000
- `just admin`: Runs the Streamlit admin app

### 5. Template Management
Parameterized project templates (using [Copier](https://copier.readthedocs.io/)) are generated from the living "Golden Master" apps in the `apps/` directory.

To update all templates after making changes to the source apps:
```bash
just gen-templates
```

### 6. Using Templates
To instantiate a new project from a template:
```bash
# Default (chainlit-chat)
just create-app

# Specific template and destination
just create-app reflex-chat my-new-project
```

The generated project will include its own `Justfile` for local development:
- `just sync`: Properly synchronizes dependencies using Python 3.13.
- `just run`: Runs the application.
