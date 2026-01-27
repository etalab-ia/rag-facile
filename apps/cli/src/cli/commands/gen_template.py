import shutil
import subprocess
from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer()
console = Console()

COPIER_YML = """project_name:
  type: str
  help: What is the name of your project?
  default: my-chainlit-app

description:
  type: str
  help: Short description of the project
  default: A Chainlit Chat Application

openai_model:
  type: str
  help: Default OpenAI model to use
  default: gpt-3.5-turbo

system_prompt:
  type: str
  help: Initial system prompt for the assistant
  default: You are a helpful assistant.

welcome_message:
  type: str
  help: Header text for the welcome screen
  default: Welcome to Chainlit! 🚀🤖
"""


@app.command()
def generate():
    """
    Generate the Chainlit Chat template using GritQL.
    Copies apps/chainlit-chat to templates/chainlit-chat and parameterizes it.
    """
    repo_root = Path.cwd()
    source = repo_root / "apps" / "chainlit-chat"
    target = repo_root / "templates" / "chainlit-chat"

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
        "chainlit_chat.egg-info",
        ".venv",
        ".env",
    ]
    for artifact in artifacts:
        path = target / artifact
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

    console.print("Applying Grit patterns...")

    # Apply Grit patterns for Python files
    grit_patterns = repo_root / ".grit" / "patterns"
    app_grit = grit_patterns / "app.grit"
    target_app_py = target / "app.py"

    subprocess.run(
        ["grit", "apply", str(app_grit), str(target_app_py), "--force"],
        check=True,
        cwd=repo_root,
    )

    # Fallback replacements for TOML/MD
    console.print("Applying fallback parameterization...")

    # Parameterize pyproject.toml
    pyproject_path = target / "pyproject.toml"
    if pyproject_path.exists():
        content = pyproject_path.read_text()
        content = content.replace('"chainlit-chat"', '"{{ project_name }}"')
        content = content.replace(
            '"Chainlit Chat with OpenAI Functions Streaming"', '"{{ description }}"'
        )
        pyproject_path.write_text(content)
        console.print("✔ pyproject.toml parameterized")

    # Parameterize chainlit.md
    md_path = target / "chainlit.md"
    if md_path.exists():
        content = md_path.read_text()
        content = content.replace(
            "# Welcome to Chainlit! 🚀🤖", "# {{ welcome_message }}"
        )
        md_path.write_text(content)
        console.print("✔ chainlit.md parameterized")

    # Generate copier.yml
    console.print("Generating copier.yml...")
    (target / "copier.yml").write_text(COPIER_YML)

    # Verification
    console.print("Verifying...")

    pyproject_valid = "{{ project_name }}" in pyproject_path.read_text()
    if pyproject_valid:
        console.print("✔ pyproject.toml validation passed")
    else:
        console.print("[red]✘ pyproject.toml validation failed[/red]")
        raise typer.Exit(code=1)

    app_py_valid = "{{ openai_model }}" in target_app_py.read_text()
    if app_py_valid:
        console.print("✔ app.py validation passed")
    else:
        console.print("[red]✘ app.py validation failed[/red]")
        raise typer.Exit(code=1)

    console.print("[green]Template generation complete![/green]")
