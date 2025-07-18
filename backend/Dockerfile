FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 
# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create and set permissions for media and static directories
RUN mkdir -p /code/media /code/static

# Collect static files
RUN python manage.py collectstatic --noinput

# Run health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Expose port
EXPOSE 8000

# Run gunicorn with appropriate settings
CMD ["gunicorn", "compliance_ai_assistant.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
