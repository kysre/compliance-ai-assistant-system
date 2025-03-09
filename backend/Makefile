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
