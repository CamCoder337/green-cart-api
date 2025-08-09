# GreenCart API Dockerfile for Render deployment
FROM python:3.11-slim

LABEL authors="CamCoder337"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DJANGO_SETTINGS_MODULE=core.settings.production_minimal \
    PATH="/home/app/.local/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libpq5 \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create and use a non-root user
RUN useradd --create-home --shell /bin/bash app
USER app
WORKDIR /home/app

# Copy requirements files
COPY --chown=app:app requirements-python311.txt requirements.txt requirements-flexible.txt requirements-minimal.txt ./

# Install dependencies with multiple fallback strategies (Python 3.11 optimized first)
RUN pip install --user -r requirements-python311.txt || \
    (echo "Python 3.11 requirements failed, trying standard..." && \
     pip install --user -r requirements.txt) || \
    (echo "Standard requirements failed, trying flexible versions..." && \
     pip install --user -r requirements-flexible.txt) || \
    (echo "Flexible requirements failed, trying minimal versions..." && \
     pip install --user -r requirements-minimal.txt) || \
    (echo "All requirements failed, installing core packages individually..." && \
     pip install --user Django djangorestframework python-decouple psycopg2-binary==2.9.7 gunicorn==21.2.0)

# Copy project files
COPY --chown=app:app . .

# Create necessary directories
RUN mkdir -p staticfiles media logs

# Skip static files collection during build (will be done at runtime with proper env vars)

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python manage.py check || exit 1

# Startup command with diagnostics, migrations, test data, and gunicorn
CMD ["sh", "-c", "echo '🚀 Starting GreenCart API...' && python diagnostic.py && python manage.py migrate --noinput && python manage.py collectstatic --noinput --clear && python create_test_data.py || true && python fix_swagger_auth.py || true && echo '🌐 Starting server on port ${PORT:-8000}...' && gunicorn --bind 0.0.0.0:${PORT:-8000} --workers ${WORKERS:-3} --timeout 120 --access-logfile - --error-logfile - core.wsgi:application"]