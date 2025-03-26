.PHONY: format format-check help imports-check imports-fix

help:
	@echo "Available commands:"
	@echo "  make format-check - Check if Python code needs formatting without making changes"
	@echo "  make format      - Format Python code using Black"
	@echo "  make imports-check - Check Python import order using isort"
	@echo "  make imports-fix - Fix Python import order using isort"

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

run_admin_local:
	DJANGO_SETTINGS_MODULE="compliance_ai_assistant.settings.development" python manage.py runserver
