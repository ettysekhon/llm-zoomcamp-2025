.PHONY: sync kernel compose-up-elastic jupyter streamlit services format lint ci clean run-vector-search

sync:
	uv sync

kernel:
	uv run ipython kernel install --user \
		--env VIRTUAL_ENV "$(CURDIR)/.venv" \
		--name llm-rag-workshop

compose-up-elastic:
	docker compose -f docker-compose.elastic-search.yml up --build

compose-up-vector:
	docker compose -f docker-compose.vector-search.yml up --build

jupyter:
	uv run --with jupyter jupyter lab

services: compose-up-elastic jupyter

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

run-vector-search:
	uv run python -m vector_search.app
