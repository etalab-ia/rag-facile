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
