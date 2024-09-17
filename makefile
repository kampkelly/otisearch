# Makefile for Bettersearch

# Set of commands to manage migrations
activate-env:
	@echo "activating env..."
	conda activate ./venv

# Set of commands to manage migrations
run-migrations:
	@echo "Running migrations..."
	alembic upgrade head

undo-migration:
	@echo "Reverting latest migration..."
	alembic downgrade -1

create-migration:
	@echo "Creating migrations..."
ifdef MANUAL
	@echo "Manual migrations..."
	alembic revision -m "$(MSG)"
else
	@echo "Autogenerate migrations... $(MSG)"
	alembic revision --autogenerate -m "$(MSG)"
endif

# Set of commands to start-app
install-old:
	@echo "Installing packages..."
	pip install -r requirements.txt

# Set of commands to start-app
install:
	@echo "Installing packages..."
	pip-compile requirements.in && pip-sync requirements.txt

start-app:
ifdef PORT
	@echo "Starting app on port ${PORT}..."
	uvicorn main:app --reload --port ${PORT}
else
	@echo "Starting app on port 8000..."
	uvicorn main:app --reload
endif

# Help command to display available commands
help:
	@echo "Available commands"
	@echo "  make run-migrations    - Run all migrations up to the latest"
	@echo "  make undo-migration    - Revert the latest migration"
	@echo "  make create-migration  - Create a new migration"
	@echo "  make install           - Install packages"
	@echo "  make start-app         - Start the FastAPI app"
	@echo "  make help              - Display this help message"
