import shutil
from enum import Enum
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


class AppType(str, Enum):
    chainlit = "chainlit-chat"
    reflex = "reflex-chat"


def _read_config(app_type: AppType) -> str:
    """Read the copier.yml content from the package resources."""
    # We assume the configs are in cli.configs package
    # This matches the file structure created: apps/cli/src/cli/configs/

    # Let's trust the file system path for this script's location
    current_dir = Path(__file__).parent
    config_dir = current_dir.parent / "configs"

    if app_type == AppType.chainlit:
        return (config_dir / "chainlit_copier.yml").read_text()
    else:
        return (config_dir / "reflex_copier.yml").read_text()


@app.command()
def generate(
    app_type: Annotated[
        AppType, typer.Option("--app", help="The application template to generate")
    ],
):
    """
    Generate a Chat app template using Copier (via GritQL/manual parameterization).
    Copies apps/<app_type> to templates/<app_type> and parameterizes it.
    """
    repo_root = Path.cwd()
    source = repo_root / "apps" / app_type.value
    target = repo_root / "templates" / app_type.value

    if not source.exists():
        console.print(f"[red]Error: Source directory {source} does not exist.[/red]")
        raise typer.Exit(code=1)

    console.print(f"Recreating {target}...")
    if target.exists():
        shutil.rmtree(target)

    # Copy source to target
    shutil.copytree(source, target)

    # Cleanup artifacts
    artifacts = [
        "__pycache__",
        "*.egg-info",
        ".venv",
        ".env",
        ".git",
        ".DS_Store",
    ]
    # Specific artifacts per app
    if app_type == AppType.reflex:
        artifacts.extend([".web", ".states"])
    else:
        artifacts.extend([".chainlit"])

    for artifact_pattern in artifacts:
        for path in target.rglob(artifact_pattern):
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

    # Fallback replacements for TOML/MD/etc
    console.print("Applying parameterization...")

    # Load Copier Config
    copier_yml = _read_config(app_type)

    # Common Parameterization

    # Parameterize pyproject.toml
    pyproject_path = target / "pyproject.toml"
    if pyproject_path.exists():
        content = pyproject_path.read_text()
        content = content.replace(f'"{app_type.value}"', '"{{ project_name }}"')
        # Description might vary, handling generic replacement if possible or specific
        if app_type == AppType.chainlit:
            content = content.replace(
                '"Chainlit Chat with OpenAI Functions Streaming"',
                '"{{ description }}"',
            )
        else:
            content = content.replace(
                '"Reflex Chat Application"', '"{{ description }}"'
            )

        # Write to .jinja file
        jinja_path = target / "pyproject.toml.jinja"
        jinja_path.write_text(content)
        # Remove original
        pyproject_path.unlink()
        console.print("✔ pyproject.toml -> pyproject.toml.jinja parameterized")

    # Rename README.md -> README.md.jinja
    readme_path = target / "README.md"
    if readme_path.exists():
        readme_path.rename(target / "README.md.jinja")
        console.print("✔ README.md -> README.md.jinja renamed")

    # Generate parameterized .env.jinja
    console.print("Generating parameterized .env.jinja...")
    # Both apps use similar env vars based on our analysis
    env_content = (
        "OPENAI_API_KEY={{ openai_api_key }}\n"
        "OPENAI_BASE_URL={{ openai_base_url }}\n"
        "OPENAI_MODEL={{ openai_model }}\n"
    )
    (target / ".env.jinja").write_text(env_content)
    console.print("✔ .env.jinja generated")

    # App Specific Parameterization
    if app_type == AppType.chainlit:
        # Parameterize chainlit.md
        md_path = target / "chainlit.md"
        if md_path.exists():
            content = md_path.read_text()
            content = content.replace(
                "# Welcome to Chainlit! 🚀🤖", "# {{ welcome_message }}"
            )
            # Write to .jinja file
            jinja_path = target / "chainlit.md.jinja"
            jinja_path.write_text(content)
            # Remove original
            md_path.unlink()
            console.print("✔ chainlit.md -> chainlit.md.jinja parameterized")

    elif app_type == AppType.reflex:
        # Parameterize rxconfig.py
        rxconfig_path = target / "rxconfig.py"
        if rxconfig_path.exists():
            content = rxconfig_path.read_text()
            # Replace app_name="reflex_chat" with jinja
            content = content.replace(
                'app_name="reflex_chat"',
                "app_name=\"{{ project_name|replace('-', '_') }}\"",
            )
            (target / "rxconfig.py.jinja").write_text(content)
            rxconfig_path.unlink()
            console.print("✔ rxconfig.py -> rxconfig.py.jinja parameterized")

        # Parameterize state.py for system_prompt
        # Path: reflex_chat/state.py

        # 1. Parameterize state.py content
        state_path = target / "reflex_chat" / "state.py"
        if state_path.exists():
            content = state_path.read_text()
            content = content.replace(
                '"You are a friendly chatbot named Reflex. Respond in markdown."',
                '"{{ system_prompt }}"',
            )
            state_path.write_text(content)  # Write back to same file, rename dir later
            console.print("✔ reflex_chat/state.py parameterized")

        # 2. Rename package directory
        pkg_dir = target / "reflex_chat"
        if pkg_dir.exists():
            # We want Copier to rename this directory based on project_name
            new_pkg_dir = target / "{{ project_name|replace('-', '_') }}"
            pkg_dir.rename(new_pkg_dir)
            console.print(f"✔ Renamed reflex_chat dir to {new_pkg_dir.name}")

    # Generate copier.yml
    console.print("Generating copier.yml...")
    (target / "copier.yml").write_text(copier_yml)

    # Verification
    console.print("Verifying...")

    pyproject_jinja = target / "pyproject.toml.jinja"
    if pyproject_jinja.exists() and "{{ project_name }}" in pyproject_jinja.read_text():
        console.print("✔ pyproject.toml.jinja verification passed")
    else:
        console.print("[red]✘ pyproject.toml.jinja verification failed[/red]")
        raise typer.Exit(code=1)

    console.print("[green]Template generation complete![/green]")
