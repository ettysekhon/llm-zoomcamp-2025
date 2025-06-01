.PHONY: sync kernel compose-up jupyter streamlit services format lint ci clean

sync:
	uv sync

kernel:
	uv run ipython kernel install --user \
		--env VIRTUAL_ENV "$(CURDIR)/.venv" \
		--name llm-rag-workshop

compose-up:
	docker compose up --build

jupyter:
	uv run --with jupyter jupyter lab

services: compose-up jupyter

streamlit:
	uv run --with streamlit streamlit run packages/llm-rag-workshop/src/llm_rag_workshop/app.py

format:
	uv run black .
	uv run ruff check . --fix

lint:
	uv run ruff check .

ci: lint

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
