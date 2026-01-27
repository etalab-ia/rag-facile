#!/bin/bash
set -e

SOURCE="apps/chainlit-chat"
TARGET="packages/templates/chainlit-chat"

echo "Recreating $TARGET..."
rm -rf "$TARGET"
mkdir -p "$TARGET"
cp -r "$SOURCE/" "$TARGET/"

# Cleanup build artifacts and temporary files
rm -rf "$TARGET/__pycache__"
rm -rf "$TARGET/chainlit_chat.egg-info"
rm -rf "$TARGET/.venv"
rm -rf "$TARGET/.env"

# Keep .chainlit as it contains config.toml

echo "Applying Grit patterns..."
# Apply patterns to specific files
# GritQL works well for Python
grit apply .grit/patterns/app.grit "$TARGET/app.py" --force

# Fallback to sed for TOML/MD where Grit parser support is limited in this environment
sed -i '' 's/"chainlit-chat"/"{{ project_name }}"/g' "$TARGET/pyproject.toml"
sed -i '' 's/"Chainlit Chat with OpenAI Functions Streaming"/"{{ description }}"/g' "$TARGET/pyproject.toml"
sed -i '' 's/# Welcome to Chainlit! 🚀🤖/# {{ welcome_message }}/g' "$TARGET/chainlit.md"

echo "Generating copier.yml..."
cat > "$TARGET/copier.yml" <<EOF
project_name:
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
EOF

echo "Template generation complete. Verifying..."
if grep -q "{{ project_name }}" "$TARGET/pyproject.toml"; then
    echo "✔ pyproject.toml parameterized successfully"
else
    echo "✘ pyproject.toml parameterization failed"
    exit 1
fi

if grep -q "{{ openai_model }}" "$TARGET/app.py"; then
    echo "✔ app.py parameterized successfully"
else
    echo "✘ app.py parameterization failed"
    exit 1
fi

echo "All checks passed."
