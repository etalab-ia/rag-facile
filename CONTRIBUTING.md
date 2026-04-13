# Contributing to Rag Facile

Welcome! This guide helps you contribute to Rag Facile, the French government RAG pipeline for PDF documents.

## Getting Started

Please refer to the [Installation section of the README](./README.md#installation) to set up your development environment.

## Creating a Branch

```bash
# Create a new branch for your feature or fix
git checkout -b feature/your-feature
```

## Development Commands

| Command | Description |
|---------|-------------|
| `pnpm dev` | Start Mastra dev server (localhost:4111) |
| `pnpm build` | Build the Mastra project |
| `pnpm start` | Start production server |
| `pnpm typecheck` | Run TypeScript type checking |
| `pnpm lint` | Check code style and formatting |
| `pnpm lint:fix` | Auto-fix lint and format issues |
| `pnpm format` | Format code with Biome |

## Pull Request Process

1. **Follow the code style** — Rag Facile uses Biome for linting and formatting
2. **Run checks locally** — Ensure `pnpm typecheck` and `pnpm lint` pass
3. **Update documentation** — If your changes affect the README or add new features
4. **Use conventional commits** — e.g., `feat: add new tool`, `fix: resolve issue`

## Testing

Please refer to the [Development Commands](#development-commands) section for the available testing and linting commands.

## Questions?

Open an issue at https://github.com/etalab-ia/rag-facile/issues