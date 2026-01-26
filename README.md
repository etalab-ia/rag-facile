# RAG Starter Kit
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

### 2. Setup
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
