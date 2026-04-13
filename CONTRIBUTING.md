# Contributing to Rag Facile

Welcome! This guide helps you contribute to Rag Facile, the French government RAG pipeline for PDF documents.

## Getting Started

```bash
# Clone the repository
git clone https://github.com/etalab-ia/rag-facile.git
cd rag-facile

# Install dependencies
pnpm install

# Start the dev server
pnpm dev
```

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

```bash
# Run type checking
pnpm typecheck

# Run linting
pnpm lint

# Fix lint issues
pnpm lint:fix
```

## Questions?

Open an issue at https://github.com/etalab-ia/rag-facile/issues