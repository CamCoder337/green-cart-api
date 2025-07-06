# Django Boilerplate Makefile
# Provides convenient commands for development and deployment

.PHONY: help install dev test clean lint format migrate run deploy

# Default target
help:
	@echo "🚀 Django Boilerplate - Available Commands"
	@echo "==========================================="
	@echo ""
	@echo "📦 Setup & Installation:"
	@echo "  make install     - Install all dependencies"
	@echo "  make dev         - Setup development environment"
	@echo "  make venv        - Create virtual environment"
	@echo ""
	@echo "🏃 Development:"
	@echo "  make run         - Run development server"
	@echo "  make migrate     - Run database migrations"
	@echo "  make superuser   - Create superuser"
	@echo "  make shell       - Open Django shell"
	@echo ""
	@echo "🧪 Testing & Quality:"
	@echo "  make test        - Run tests"
	@echo "  make test-cov    - Run tests with coverage"
	@echo "  make lint        - Run linting checks"
	@echo "  make format      - Format code with black"
	@echo "  make check       - Run all quality checks"
	@echo ""
	@echo "🛠️ Database:"
	@echo "  make makemigrations - Create new migrations"
	@echo "  make migrate     - Apply migrations"
	@echo "  make resetdb     - Reset database (⚠️  destructive)"
	@echo ""
	@echo "🚀 Deployment:"
	@echo "  make deploy      - Deploy to production"
	@echo "  make collect     - Collect static files"
	@echo ""
	@echo "🧹 Maintenance:"
	@echo "  make clean       - Clean temporary files"
	@echo "  make update-deps - Update dependencies"
	@echo ""

# Variables
PYTHON = python
PIP = pip
MANAGE = $(PYTHON) manage.py
VENV_DIR = venv

# Check if virtual environment is activated
ifdef VIRTUAL_ENV
    VENV_ACTIVE = true
else
    VENV_ACTIVE = false
endif

# Setup & Installation
venv:
	@echo "🐍 Creating virtual environment..."
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "✅ Virtual environment created!"
	@echo "💡 Activate it with: source $(VENV_DIR)/bin/activate"

install:
	@echo "📦 Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "✅ Dependencies installed!"

dev: install
	@echo "🛠️ Setting up development environment..."
	$(PIP) install -r requirements-dev.txt
	@echo "✅ Development environment ready!"

# Development
run:
	@echo "🏃 Starting development server..."
	$(MANAGE) runserver

migrate:
	@echo "🗄️ Running database migrations..."
	$(MANAGE) migrate

makemigrations:
	@echo "📝 Creating new migrations..."
	$(MANAGE) makemigrations

superuser:
	@echo "👑 Creating superuser..."
	$(MANAGE) createsuperuser

shell:
	@echo "🐚 Opening Django shell..."
	$(MANAGE) shell_plus --ipython

# Testing & Quality
test:
	@echo "🧪 Running tests..."
	$(MANAGE) test

test-cov:
	@echo "🧪 Running tests with coverage..."
	pytest --cov=. --cov-report=html --cov-report=term

lint:
	@echo "🔍 Running linting checks..."
	flake8 .
	@echo "✅ Linting completed!"

format:
	@echo "🎨 Formatting code..."
	black .
	isort .
	@echo "✅ Code formatted!"

check: lint
	@echo "✅ Running Django system checks..."
	$(MANAGE) check
	@echo "✅ All checks passed!"

# Database
resetdb:
	@echo "⚠️  Resetting database (this will delete all data)..."
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo ""; \
		rm -f db.sqlite3; \
		$(MANAGE) migrate; \
		echo "✅ Database reset completed!"; \
	else \
		echo ""; \
		echo "❌ Operation cancelled."; \
	fi

# Deployment
collect:
	@echo "📦 Collecting static files..."
	$(MANAGE) collectstatic --noinput

deploy: collect
	@echo "🚀 Deploying to production..."
	# Add your deployment commands here
	@echo "✅ Deployment completed!"

# Maintenance
clean:
	@echo "🧹 Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .tox/
	@echo "✅ Cleanup completed!"

update-deps:
	@echo "🔄 Updating dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade -r requirements.txt
	$(PIP) install --upgrade -r requirements-dev.txt
	@echo "✅ Dependencies updated!"

# Docker commands
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t django-boilerplate .
	@echo "✅ Docker image built!"

docker-run:
	@echo "🐳 Running Docker container..."
	docker-compose up -d
	@echo "✅ Docker container started!"

docker-stop:
	@echo "🐳 Stopping Docker container..."
	docker-compose down
	@echo "✅ Docker container stopped!"

# CLI testing
test-cli:
	@echo "🧪 Testing CLI tool..."
	python create_django_project.py test_project --no-git --no-venv --no-deps
	@echo "✅ CLI test completed!"
	rm -rf test_project

# Pre-commit hooks
install-hooks:
	@echo "🪝 Installing pre-commit hooks..."
	pre-commit install
	@echo "✅ Pre-commit hooks installed!"

# Help for specific commands
help-install:
	@echo "📦 INSTALL COMMAND"
	@echo "=================="
	@echo "Installs all production dependencies from requirements.txt"
	@echo ""
	@echo "Usage: make install"
	@echo ""
	@echo "This command will:"
	@echo "  • Upgrade pip to latest version"
	@echo "  • Install all packages from requirements.txt"

help-dev:
	@echo "🛠️ DEV COMMAND"
	@echo "=============="
	@echo "Sets up complete development environment"
	@echo ""
	@echo "Usage: make dev"
	@echo ""
	@echo "This command will:"
	@echo "  • Run 'make install' first"
	@echo "  • Install development dependencies"
	@echo "  • Setup debugging tools"