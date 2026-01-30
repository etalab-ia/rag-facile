default:
	@just --list

# Run the Reflex Chat application
reflex-chat:
	cd apps/reflex-chat && uv run reflex run

# Run the ChainLit Chat application
chainlit-chat:
        cd apps/chainlit-chat && uv run chainlit run app.py -w

# Run the Streamlit Admin application
admin:
        cd apps/admin && uv run streamlit run src/admin/main.py

# Install all dependencies and setup the workspace
setup:
        uv sync
        uv lock

# Generate all app templates
gen-templates:
        uv run --project apps/cli rf template generate --app chainlit-chat
        uv run --project apps/cli rf template generate --app reflex-chat

# Create a new application from a template using Copier
# Usage: just create-app [app-type] [destination]
create-app app_type="chainlit-chat" destination="":
        #!/usr/bin/env bash
        set -euo pipefail
        TYPE="{{app_type}}"
        # Normalize input
        if [[ "$TYPE" == "chainlit" ]] || [[ "$TYPE" == "chainlit-app" ]]; then TYPE="chainlit-chat"; fi
        if [[ "$TYPE" == "reflex" ]] || [[ "$TYPE" == "reflex-app" ]]; then TYPE="reflex-chat"; fi

        if [ "$TYPE" != "chainlit-chat" ] && [ "$TYPE" != "reflex-chat" ]; then
            echo "Error: Invalid app type '{{app_type}}'. Valid options are: chainlit-chat, reflex-chat (or shorthands like 'chainlit', 'reflex')"
            exit 1
        fi

        if [ ! -d "templates/$TYPE" ]; then just gen-templates; fi

        # Check for API Key in environment
        API_KEY_ARG=""
        if [ -n "${ALBERT_API_KEY:-}" ]; then
            API_KEY_ARG="-d openai_api_key=$ALBERT_API_KEY"
            echo "Using ALBERT_API_KEY from environment"
        elif [ -n "${OPENAI_API_KEY:-}" ]; then
            API_KEY_ARG="-d openai_api_key=$OPENAI_API_KEY"
            echo "Using OPENAI_API_KEY from environment"
        fi

        uv run copier copy $API_KEY_ARG templates/"$TYPE" "{{if destination == "" { "$TYPE" } else { destination}}}"
