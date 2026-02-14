.PHONY: run_chainlit
run_chainlit:
	chainlit run backend/app.py -w

.PHONY: init-db
init-db:
	uv run python scripts/init_db.py

.PHONY: test-db
test-db:
	uv run python -c "from infrastructure.database.connection import get_connection, init_database; init_database(); print('Database OK')"

.PHONY: format
format:
	uv run black src/ tests/ scripts/

.PHONY: lint
lint:
	uv run ruff check src/ tests/ scripts/

.PHONY: pre-commit
pre-commit:
	uv run pre-commit run --all-files

.SILENT .PHONY: clear_pycache
clear_pycache:
	find src/ tests/ -name "__pycache__" -exec rm -rf {} \;

.PHONY: help
help:
	@echo "Available commands:"
	@echo "  run_chainlit  - Run the chainlit application"
	@echo "  init-db       - Initialize the database"
	@echo "  test-db       - Test database connection"
	@echo "  format        - Format code with black"
	@echo "  lint          - Run ruff linting"
	@echo "  pre-commit    - Run pre-commit hooks"
	@echo "  clear_pycache - Clear Python cache files"
	@echo "  help          - Show this help message"
