# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GreenCart is a Django-based REST API for connecting local producers with eco-conscious consumers. The project follows Django best practices with modular settings, Django REST Framework for APIs, and comprehensive development tools.

## Architecture

### Core Structure
- **Django 5.2.4** with **Python 3.13+**
- **Modular settings**: `core/settings/` contains base.py, development.py, production.py, testing.py
- **Custom User Model**: `accounts.User` extends AbstractUser with email authentication
- **REST API**: Django REST Framework with token authentication
- **Database**: SQLite (development), PostgreSQL (production)
- **Caching**: Redis support with local memory fallback

### Key Applications
- `accounts/`: Custom user management with email-based authentication
- `api/`: Main API endpoints and REST framework configuration
- `core/`: Project configuration and settings management

### Settings Configuration
The project uses environment-specific settings:
- `DJANGO_SETTINGS_MODULE=core.settings.development` (default)
- `DJANGO_SETTINGS_MODULE=core.settings.production` (production)
- `DJANGO_SETTINGS_MODULE=core.settings.testing` (tests)

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python3.13 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
make dev                    # Development setup with all tools
make install               # Production dependencies only
pip install -r requirements-dev.txt  # Manual installation
```

### Development Server
```bash
make run                   # Start development server
python manage.py runserver # Direct command
```

### Database Operations
```bash
make makemigrations        # Create new migrations
make migrate              # Apply migrations
make resetdb              # Reset database (destructive)
python manage.py migrate  # Direct migration command
```

### Code Quality & Testing
```bash
make test                 # Run Django tests
make test-cov            # Run pytest with coverage
pytest                   # Direct pytest command
make lint                # Run flake8 linting
make format              # Format with black + isort
make check               # Run Django system checks
```

### Development Tools
```bash
make shell               # Django shell with shell_plus
make superuser          # Create superuser
python manage.py shell_plus --ipython  # Enhanced Django shell
```

### Docker Development
```bash
make docker-build        # Build Docker image
make docker-run         # Start with docker-compose
make docker-stop        # Stop containers
```

## API Architecture

### Authentication
- **Token Authentication**: Primary method using DRF tokens
- **Session Authentication**: Available for browser-based access
- **Custom User Model**: Email-based authentication instead of username

### REST Framework Configuration
- **Pagination**: 20 items per page (configurable via `DRF_PAGE_SIZE`)
- **Filtering**: django-filter, search, and ordering backends enabled
- **Permissions**: `IsAuthenticated` by default
- **Renderers**: JSON only (production-ready)

### CORS Configuration
- Configured for React frontend on `http://localhost:3000`
- Credentials allowed for authentication

## File Structure Patterns

### Models
- Custom User model in `accounts/models.py` extends AbstractUser
- Uses UUID primary keys for most models (prepare for this pattern)
- Database indexes on commonly queried fields

### Settings Management
- Environment variables loaded via `python-decouple`
- Database URL parsing via `dj-database-url`
- Separate files for different environments in `core/settings/`

### Static Files
- **WhiteNoise** for static file serving
- **Pillow** for image processing
- Compressed manifest storage for production

## Environment Variables

Key environment variables (see `.env.example`):
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (False in production)
- `DATABASE_URL`: Database connection string
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `CORS_ALLOWED_ORIGINS`: Frontend URLs for CORS

## Testing

### Framework
- **pytest** with **pytest-django** for testing
- **factory-boy** for test data generation
- **coverage** for code coverage reporting

### Test Commands
```bash
pytest                           # Run all tests
pytest apps/accounts/tests/      # Run specific app tests
pytest --cov=. --cov-report=html # Coverage report
python manage.py test           # Django's test runner
```

## Production Considerations

### Deployment
- **Gunicorn** configured as WSGI server  
- **WhiteNoise** for static file serving
- **Redis** for caching and session storage
- PostgreSQL database recommended

### Security
- CSRF and session cookie security configured
- Security middleware enabled
- Environment-based security settings

## Code Quality Tools

- **Black**: Code formatting (line length 88)
- **isort**: Import sorting  
- **flake8**: Linting and style checking
- **mypy**: Type checking with django-stubs
- **pre-commit**: Git hooks for code quality

When making changes, always run `make format` and `make lint` before committing.