# Run the Reflex Chat application
reflex-chat:
	cd apps/reflex-chat && uv run reflex run

# Run the ChainLit Chat application
chat:
	cd apps/chat && uv run chainlit run src/chat/app.py

# Run the Streamlit Admin application
admin:
	cd apps/admin && uv run streamlit run src/admin/main.py

# Install all dependencies and setup the workspace
setup:
	uv sync
	uv lock
