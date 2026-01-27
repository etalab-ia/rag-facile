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
        @if [ "{{app_type}}" != "chainlit-chat" ] && [ "{{app_type}}" != "reflex-chat" ]; then \
            echo "Error: Invalid app type '{{app_type}}'. Valid options are: chainlit-chat, reflex-chat"; \
            exit 1; \
        fi
        @if [ ! -d "templates/{{app_type}}" ]; then just gen-templates; fi
        uv run copier copy templates/{{app_type}} {{if destination == "" { app_type } else { destination}}}
