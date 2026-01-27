import shutil
import subprocess
from pathlib import Path

import libcst as cst
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

openai_api_key:
  type: str
  help: What is your OpenAI API Key? (Get one at https://albert.sites.beta.gouv.fr/access/)

openai_base_url:
  type: str
  help: What is your OpenAI Base URL?
  default: https://albert.api.etalab.gouv.fr/v1

openai_model:
  type: str
  help: Default OpenAI model to use
  default: openweight-large

system_prompt:
  type: str
  help: Initial system prompt for the assistant
  default: You are a helpful assistant.

welcome_message:
  type: str
  help: Header text for the welcome screen
  default: Welcome to Chainlit! 🚀🤖
"""

# Placeholders to maintain valid Python syntax during CST pass
PLACEHOLDERS = {
    "chainlit_chat": "__PROJECT_SLUG_PLACEHOLDER__",
    "reflex_chat": "__PROJECT_SLUG_PLACEHOLDER__",
}


class JinjaTransformer(cst.CSTTransformer):
    """
    LibCST Transformer to parameterize Python code.
    Phase 1: Semantic Preparation
    """

    def __init__(self, mappings: dict[str, str]):
        self.mappings = mappings

    def leave_SimpleString(
        self, original_node: cst.SimpleString, updated_node: cst.SimpleString
    ) -> cst.SimpleString:
        # Parameterize strings
        val = updated_node.value
        for golden, tag in self.mappings.items():
            if golden in val:
                # Replace golden value with Jinja tag inside the string
                new_val = val.replace(golden, tag)
                return updated_node.with_changes(value=new_val)
        return updated_node

    def leave_Name(self, original_node: cst.Name, updated_node: cst.Name) -> cst.Name:
        # Parameterize identifiers using placeholders
        if updated_node.value in PLACEHOLDERS:
            return updated_node.with_changes(value=PLACEHOLDERS[updated_node.value])
        return updated_node


def run_ast_grep(target_dir: Path, pattern: str, rewrite: str):
    """Run ast-grep (sg) via pnpx for structural search and replace."""
    try:
        subprocess.run(
            [
                "pnpm",
                "--package=@ast-grep/cli",
                "dlx",
                "sg",
                "run",
                "--pattern",
                pattern,
                "--rewrite",
                rewrite,
                "-U",
            ],
            cwd=target_dir,
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        msg = (
            f"[yellow]Warning: ast-grep failed for {pattern}: "
            f"{e.stderr.decode()}[/yellow]"
        )
        console.print(msg)


@app.command()
def generate():
    """
    Generate the Chainlit Chat template using a Hybrid LibCST + ast-grep pipeline.
    Copies apps/chainlit-chat to templates/chainlit-chat and parameterizes it.
    """
    # Robustly find repo root (assumes gen_template.py is in apps/cli/src/cli/commands/)
    repo_root = Path(__file__).resolve().parents[5]
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
    artifacts = ["__pycache__", "chainlit_chat.egg-info", ".venv", ".env"]
    for artifact in artifacts:
        path = target / artifact
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

    console.print("Applying parameterization pipeline...")

    # Phase 1: Semantic Preparation with LibCST
    mappings = {
        "chainlit-chat": "{{ project_name }}",
        "Chainlit Chat with OpenAI Functions Streaming": ("{{ description }}"),
        "You are a helpful assistant.": "{{ system_prompt }}",
        "Welcome to Chainlit! 🚀🤖": "{{ welcome_message }}",
    }

    python_files = list(target.rglob("*.py"))
    for py_file in python_files:
        code = py_file.read_text()
        tree = cst.parse_module(code)
        transformer = JinjaTransformer(mappings)
        modified_tree = tree.visit(transformer)
        py_file.write_text(modified_tree.code)
        console.print(f"✔ LibCST pass applied to {py_file.name}")

    # Phase 2: Structural Injection with ast-grep / Text Replacement
    # Inject actual Jinja tags where LibCST placeholders were used
    for golden, placeholder in PLACEHOLDERS.items():
        # Using ast-grep for identifier replacement is safer than global text replace
        run_ast_grep(target, placeholder, "{{ project_name | replace('-', '_') }}")

    # Phase 3: Non-Python files (TOML, MD)
    # Parameterize pyproject.toml
    pyproject_path = target / "pyproject.toml"
    if pyproject_path.exists():
        content = pyproject_path.read_text()
        content = content.replace('"chainlit-chat"', '"{{ project_name }}"')
        msg = "Chainlit Chat with OpenAI Functions Streaming"
        content = content.replace(f'"{msg}"', '"{{ description }}"')
        (target / "pyproject.toml.jinja").write_text(content)
        pyproject_path.unlink()
        console.print("✔ pyproject.toml -> pyproject.toml.jinja parameterized")

    # Parameterize chainlit.md
    md_path = target / "chainlit.md"
    if md_path.exists():
        content = md_path.read_text()
        content = content.replace(
            "# Welcome to Chainlit! 🚀🤖", "# {{ welcome_message }}"
        )
        (target / "chainlit.md.jinja").write_text(content)
        md_path.unlink()
        console.print("✔ chainlit.md -> chainlit.md.jinja parameterized")

    # Rename README.md -> README.md.jinja
    readme_path = target / "README.md"
    if readme_path.exists():
        readme_path.rename(target / "README.md.jinja")
        console.print("✔ README.md -> README.md.jinja renamed")

    # Phase 4: Metadata Generation
    console.print("Generating metadata...")
    env_content = (
        "OPENAI_API_KEY={{ openai_api_key }}\n"
        "OPENAI_BASE_URL={{ openai_base_url }}\n"
        "OPENAI_MODEL={{ openai_model }}\n"
    )
    (target / ".env.jinja").write_text(env_content)
    (target / "copier.yml").write_text(COPIER_YML)

    console.print("[green]Template generation complete with Hybrid Pipeline![/green]")


if __name__ == "__main__":
    generate()
