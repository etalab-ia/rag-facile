import shutil
import subprocess
from enum import Enum
from pathlib import Path
from typing import Annotated

import libcst as cst
import typer
from rich.console import Console

app = typer.Typer()
console = Console()


class AppType(str, Enum):
    chainlit = "chainlit-chat"
    reflex = "reflex-chat"


def _read_config(app_type: AppType) -> str:
    """Read the copier.yml content from the package resources."""
    # Robustly find repo root (assumes gen_template.py is in apps/cli/src/cli/commands/)
    repo_root = Path(__file__).resolve().parents[5]
    config_dir = repo_root / "apps" / "cli" / "src" / "cli" / "configs"

    if app_type == AppType.chainlit:
        return (config_dir / "chainlit_copier.yml").read_text()
    else:
        return (config_dir / "reflex_copier.yml").read_text()


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
                ".",
            ],
            cwd=target_dir,
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        # sg returns 1 if no matches are found, which we want to ignore
        if e.returncode == 1 and not e.stderr.decode().strip():
            return

        msg = (
            f"[yellow]Warning: ast-grep failed for {pattern}: "
            f"{e.stderr.decode().strip()}[/yellow]"
        )
        console.print(msg)


@app.command()
def generate(
    app_type: Annotated[
        AppType, typer.Option("--app", help="The application template to generate")
    ],
):
    """
    Generate a Chat app template using a Hybrid LibCST + ast-grep pipeline.
    Copies apps/<app_type> to templates/<app_type> and parameterizes it.
    """
    # Robustly find repo root (assumes gen_template.py is in apps/cli/src/cli/commands/)
    repo_root = Path(__file__).resolve().parents[5]
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

    console.print("Applying parameterization pipeline...")

    # Phase 1: Semantic Preparation with LibCST
    mappings = {
        app_type.value: "{{ project_name }}",
        app_type.value.replace("-", "_"): "{{ project_name | replace('-', '_') }}",
        "You are a helpful assistant.": "{{ system_prompt }}",
        "You are a friendly chatbot named Reflex. Respond in markdown.": (
            "{{ system_prompt }}"
        ),
    }

    if app_type == AppType.chainlit:
        mappings.update(
            {
                "Chainlit Chat with OpenAI Functions Streaming": "{{ description }}",
                "Welcome to Chainlit! 🚀🤖": "{{ welcome_message }}",
            }
        )
    else:
        mappings.update(
            {
                "Reflex Chat Application": "{{ description }}",
            }
        )

    python_files = list(target.rglob("*.py"))
    for py_file in python_files:
        code = py_file.read_text()
        try:
            tree = cst.parse_module(code)
            transformer = JinjaTransformer(mappings)
            modified_tree = tree.visit(transformer)
            py_file.write_text(modified_tree.code)
            console.print(f"✔ LibCST pass applied to {py_file.name}")
        except Exception as e:
            console.print(
                f"[yellow]Warning: LibCST failed for {py_file.name}: {e}[/yellow]"
            )

    # Phase 2: Structural Injection with ast-grep
    # Inject actual Jinja tags where LibCST placeholders were used
    for placeholder in set(PLACEHOLDERS.values()):
        run_ast_grep(target, placeholder, "{{ project_name | replace('-', '_') }}")

    # Phase 3: App-Specific Parameterization and Metadata
    copier_yml = _read_config(app_type)

    # Parameterize pyproject.toml
    pyproject_path = target / "pyproject.toml"
    if pyproject_path.exists():
        content = pyproject_path.read_text()
        content = content.replace(f'"{app_type.value}"', '"{{ project_name }}"')
        if app_type == AppType.chainlit:
            msg = "Chainlit Chat with OpenAI Functions Streaming"
            content = content.replace(f'"{msg}"', '"{{ description }}"')
        else:
            content = content.replace(
                '"Reflex Chat Application"', '"{{ description }}"'
            )

        (target / "pyproject.toml.jinja").write_text(content)
        pyproject_path.unlink()
        console.print("✔ pyproject.toml -> pyproject.toml.jinja parameterized")

    # Rename README.md -> README.md.jinja
    readme_path = target / "README.md"
    if readme_path.exists():
        readme_path.rename(target / "README.md.jinja")
        console.print("✔ README.md -> README.md.jinja renamed")

    # Generate parameterized .env.jinja
    console.print("Generating parameterized .env.jinja...")
    env_content = (
        "OPENAI_API_KEY={{ openai_api_key }}\n"
        "OPENAI_BASE_URL={{ openai_base_url }}\n"
        "OPENAI_MODEL={{ openai_model }}\n"
    )
    (target / ".env.jinja").write_text(env_content)

    if app_type == AppType.chainlit:
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

    elif app_type == AppType.reflex:
        # Parameterize rxconfig.py
        rxconfig_path = target / "rxconfig.py"
        if rxconfig_path.exists():
            content = rxconfig_path.read_text()
            content = content.replace(
                'app_name="reflex_chat"',
                "app_name=\"{{ project_name|replace('-', '_') }}\"",
            )
            (target / "rxconfig.py.jinja").write_text(content)
            rxconfig_path.unlink()
            console.print("✔ rxconfig.py -> rxconfig.py.jinja parameterized")

        # Reflex specific directory renames and file extensions
        pkg_dir = target / "reflex_chat"
        if pkg_dir.exists():
            # Rename all .py files to .py.jinja in the package dir
            for py_file in pkg_dir.rglob("*.py"):
                py_file.rename(py_file.with_suffix(".py.jinja"))

            # Rename main app file
            main_app_jinja = pkg_dir / "reflex_chat.py.jinja"
            if main_app_jinja.exists():
                new_app_name = "{{ project_name|replace('-', '_') }}.py.jinja"
                main_app_jinja.rename(pkg_dir / new_app_name)

            # Rename package directory
            new_pkg_dir = target / "{{ project_name|replace('-', '_') }}"
            pkg_dir.rename(new_pkg_dir)
            console.print("✔ Reflex package structure parameterized")

    # Generate copier.yml
    console.print("Generating copier.yml...")
    (target / "copier.yml").write_text(copier_yml)

    console.print(f"[green]Template generation complete for {app_type.value}![/green]")


if __name__ == "__main__":
    generate()
