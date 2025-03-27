.PHONY: format format-check help imports-check imports-fix

help:
	@echo "Available commands:"
	@echo "  make format-check      - Check if Python code needs formatting without making changes"
	@echo "  make format            - Format Python code using Black"
	@echo "  make imports-check     - Check Python import order using isort"
	@echo "  make imports-fix       - Fix Python import order using isort"
	@echo "  make messages          - Compile translation messages"
	@echo "  make migrations        - Make migrations & migrate database"
	@echo "  make run-admin-local   - Run the admin interface locally"
	@echo "  make import-rules      - Import rules data from JSON file into GraphRAG service (BATCH_SIZE=50 LIMIT=200)"

format-check:
	@echo "Checking Python code formatting with Black..."
	black --check .

format-fix:
	@echo "Formatting Python code with Black..."
	black .
	@echo "Formatting completed!"

imports-check:
	@echo "Checking Python import order with isort..."
	isort --check --diff --profile black .

imports-fix:
	@echo "Fixing Python import order with isort..."
	isort --profile black .
	@echo "Import ordering completed!"

install:
	pip install --upgrade pip
	pip install -r requirements.txt

messages:
	python manage.py compilemessages -l fa

migrations:
	DJANGO_SETTINGS_MODULE="compliance_ai_assistant.settings.development" python manage.py makemigrations
	DJANGO_SETTINGS_MODULE="compliance_ai_assistant.settings.development" python manage.py migrate

run-admin-local:
	DJANGO_SETTINGS_MODULE="compliance_ai_assistant.settings.development" python manage.py runserver

import-rules:
	@echo "Importing rules data into GraphRAG service..."
	DJANGO_SETTINGS_MODULE="compliance_ai_assistant.settings.development" python manage.py import_rules $(if $(BATCH_SIZE),--batch-size=$(BATCH_SIZE),) $(if $(LIMIT),--limit=$(LIMIT),)
	@echo "Import process completed!"
