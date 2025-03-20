.PHONY: format format-check help

help:
	@echo "Available commands:"
	@echo "  make format      - Format Python code using Black"
	@echo "  make format-check - Check if Python code needs formatting without making changes"

format:
	@echo "Formatting Python code with Black..."
	black .
	@echo "Formatting completed!"

format-check:
	@echo "Checking Python code formatting with Black..."
	black --check .

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
