"""Initialize a new RAG Facile monorepo workspace."""

import re
import shutil
from pathlib import Path
from typing import Annotated

import typer
import yaml
from rich.console import Console

app = typer.Typer()
console = Console()

# Source templates from the rag-facile package
TEMPLATES_SOURCE = Path(__file__).resolve().parents[5] / ".moon" / "templates"


def _slugify(name: str) -> str:
    """Convert a name to a valid Python package name (PEP 508 compliant)."""
    # Lowercase and replace spaces/underscores with hyphens
    slug = name.lower().replace(" ", "-").replace("_", "-")
    # Remove any characters that aren't alphanumeric or hyphens
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    # Collapse multiple hyphens
    slug = re.sub(r"-+", "-", slug)
    # Strip leading/trailing hyphens
    slug = slug.strip("-")
    return slug or "my-project"


def _get_workspace_yml() -> str:
    """Generate the .moon/workspace.yml content."""
    config = {
        "projects": ["apps/*", "packages/*"],
        "vcs": {"manager": "git", "defaultBranch": "main"},
        "telemetry": False,
        "generator": {"templates": [".moon/templates"]},
    }
    return yaml.dump(config, sort_keys=False, allow_unicode=True)


def _get_toolchain_yml(python_version: str = "3.13") -> str:
    """Generate the .moon/toolchain.yml content."""
    config = {
        "$schema": "https://moonrepo.dev/schemas/toolchain.json",
        "python": {"version": python_version, "packageManager": "uv"},
    }
    return yaml.dump(config, sort_keys=False, allow_unicode=True)


def _get_pyproject_toml(project_name: str, python_version: str = "3.13") -> str:
    """Generate the root pyproject.toml content."""
    return f'''[project]
name = "{project_name}"
version = "0.1.0"
description = "RAG application built with RAG Facile"
readme = "README.md"
requires-python = ">={python_version}, <3.14"
dependencies = []

[dependency-groups]
dev = [
    "ruff>=0.14.14",
    "pre-commit>=4.0.1",
]

[tool.uv.workspace]
members = ["apps/*", "packages/*"]
'''


def _get_readme(project_name: str) -> str:
    """Generate a basic README.md."""
    return f"""# {project_name}

A RAG application built with [RAG Facile](https://github.com/etalab-ia/rag-facile).

## Getting Started

### Prerequisites

- [moon](https://moonrepo.dev/docs/install) - Repository management
- [uv](https://docs.astral.sh/uv/getting-started/installation/) - Python package manager

### Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Generate a chat application:
   ```bash
   moon generate chainlit-chat ./apps
   # or
   moon generate reflex-chat ./apps
   ```

3. Run your application (after generating):
   ```bash
   cd apps/<your-app-name>
   uv run chainlit run app.py  # for chainlit
   # or
   uv run reflex run  # for reflex
   ```

## Project Structure

```
{project_name}/
├── .moon/
│   ├── templates/       # Moon templates for generating apps
│   ├── toolchain.yml    # Python/tooling configuration
│   └── workspace.yml    # Workspace configuration
├── apps/                # Application projects
├── packages/            # Shared packages
└── pyproject.toml       # Root project configuration
```

## Available Templates

- **chainlit-chat**: A Chainlit-based chat application with OpenAI integration
- **reflex-chat**: A Reflex-based chat application

## License

MIT
"""


def _get_gitignore() -> str:
    """Generate a .gitignore file."""
    return """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
*.egg
.eggs/

# Virtual environments
.venv/
venv/
ENV/

# Environment variables
.env
.env.local

# IDEs
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Moon
.moon/cache/

# Reflex
.web/
.states/

# Chainlit
.chainlit/
.files/

# Build artifacts
dist/
build/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Logs
*.log
"""


def _get_ruff_toml() -> str:
    """Generate ruff.toml configuration."""
    return """line-length = 88
target-version = "py313"

[lint]
select = ["E", "F", "I", "UP"]
ignore = []

[format]
quote-style = "double"
"""


@app.command()
def init(
    path: Annotated[
        Path,
        typer.Argument(
            help="Directory to initialize the project in (default: current dir)"
        ),
    ] = Path("."),
    name: Annotated[
        str | None,
        typer.Option("--name", "-n", help="Project name (defaults to directory name)"),
    ] = None,
    python_version: Annotated[
        str,
        typer.Option("--python", "-p", help="Python version to use (e.g., 3.13, 3.14)"),
    ] = "3.13",
    force: Annotated[
        bool,
        typer.Option(
            "--force", "-f", help="Overwrite existing files without prompting"
        ),
    ] = False,
):
    """
    Initialize a new RAG Facile monorepo workspace.

    This command sets up a new project with moonrepo for workspace management
    and uv for Python package management. After initialization, you can use
    'moon generate' to add chat applications and other components.

    Examples:
        rf init                      # Initialize in current directory
        rf init my-rag-app           # Create and initialize new directory
        rf init . --name my-project  # Initialize current dir with specific name
    """
    # Keep original path for display, resolved path for operations
    display_path = path.absolute()
    target = path.resolve()

    # Determine project name (must be valid package name)
    raw_name = name or target.name
    if not raw_name or raw_name == ".":
        raw_name = target.parent.name if target.name == "." else target.name
    project_name = _slugify(raw_name)

    # Create target directory if it doesn't exist
    if not target.exists():
        target.mkdir(parents=True)
        console.print(f"Created directory: {display_path}")
    elif any(target.iterdir()) and not force:
        # Check if directory is not empty
        if not typer.confirm(
            f"Directory {display_path} is not empty. Continue anyway?", default=False
        ):
            raise typer.Exit(code=1)

    console.print(
        f"\n[bold blue]Initializing RAG Facile project: {project_name}[/bold blue]"
    )
    if raw_name != project_name:
        console.print(f'  [dim](slugified from "{raw_name}")[/dim]')
    console.print()

    # Create directory structure
    dirs_to_create = [
        target / ".moon" / "templates",
        target / "apps",
        target / "packages",
    ]
    for dir_path in dirs_to_create:
        dir_path.mkdir(parents=True, exist_ok=True)
        console.print(f"  [dim]Created:[/dim] {dir_path.relative_to(target)}/")

    # Generate configuration files
    files_to_create = {
        ".moon/workspace.yml": _get_workspace_yml(),
        ".moon/toolchain.yml": _get_toolchain_yml(python_version),
        "pyproject.toml": _get_pyproject_toml(project_name, python_version),
        "README.md": _get_readme(project_name),
        ".gitignore": _get_gitignore(),
        "ruff.toml": _get_ruff_toml(),
    }

    for file_path, content in files_to_create.items():
        full_path = target / file_path
        if full_path.exists() and not force:
            if not typer.confirm(f"Overwrite {file_path}?", default=False):
                console.print(f"  [yellow]Skipped:[/yellow] {file_path}")
                continue
        full_path.write_text(content)
        console.print(f"  [green]Created:[/green] {file_path}")

    # Copy templates from rag-facile package
    if TEMPLATES_SOURCE.exists():
        templates_target = target / ".moon" / "templates"
        for template_dir in TEMPLATES_SOURCE.iterdir():
            if template_dir.is_dir():
                dest = templates_target / template_dir.name
                if dest.exists():
                    if force or typer.confirm(
                        f"Overwrite template {template_dir.name}?", default=True
                    ):
                        shutil.rmtree(dest)
                    else:
                        console.print(
                            f"  [yellow]Skipped:[/yellow] template {template_dir.name}"
                        )
                        continue
                shutil.copytree(template_dir, dest)
                console.print(f"  [green]Copied:[/green] template {template_dir.name}")
    else:
        console.print(
            "\n[yellow]Warning:[/yellow] Could not find templates source. "
            "Templates will need to be added manually."
        )

    # Initialize git if not already a git repo
    git_dir = target / ".git"
    if not git_dir.exists():
        import subprocess

        try:
            subprocess.run(["git", "init"], cwd=target, check=True, capture_output=True)
            console.print("  [green]Initialized:[/green] git repository")
        except (subprocess.CalledProcessError, FileNotFoundError):
            console.print(
                "  [yellow]Warning:[/yellow] Could not initialize git repository"
            )

    # Print next steps
    console.print(
        f"\n[bold green]Success![/bold green] Project initialized at {display_path}\n"
    )
    console.print("[bold]Next steps:[/bold]")
    try:
        relative_path = display_path.relative_to(Path.cwd())
        cd_path = str(relative_path) if relative_path != Path(".") else "."
    except ValueError:
        cd_path = str(display_path)
    console.print(f"  1. cd {cd_path}")
    console.print("  2. uv sync")
    console.print("  3. moon generate chainlit-chat ./apps")
    console.print("     # or: moon generate reflex-chat ./apps")
    console.print("")


if __name__ == "__main__":
    app()
