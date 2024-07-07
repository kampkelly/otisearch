# Makefile for Bettersearch

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
	alembic revision -m "$(MSG)"
else
	alembic revision --autogenerate -m "$(MSG)"
endif

# Set of commands to start-app
install:
	@echo "Installing packages..."
	pip install -r requirements.txt

start-app:
	@echo "Starting app..."
	uvicorn main:app --reload

# Help command to display available commands
help:
	@echo "Available commands"
	@echo "  make run-migrations    - Run all migrations up to the latest"
	@echo "  make undo-migration    - Revert the latest migration"
	@echo "  make create-migration  - Create a new migration"
	@echo "  make install           - Install packages"
	@echo "  make start-app         - Start the FastAPI app"
	@echo "  make help              - Display this help message"
