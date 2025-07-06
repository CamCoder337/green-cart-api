#!/bin/bash
# Django Boilerplate CLI for Unix/Linux/macOS
# Usage: ./create_project.sh <project_name>

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Functions for colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

print_step() {
    echo -e "${CYAN}[$1/$2] $3${NC}"
}

# Check if project name is provided
if [ $# -eq 0 ]; then
    print_error "Project name is required"
    echo ""
    echo "Usage: $0 <project_name> [options]"
    echo "Example: $0 myproject"
    echo ""
    echo "Options:"
    echo "  --database postgresql    Use PostgreSQL instead of SQLite"
    echo "  --no-venv               Skip virtual environment creation"
    echo "  --no-deps               Skip dependency installation"
    echo "  --repo-url <url>        Custom repository URL"
    exit 1
fi

PROJECT_NAME="$1"
DATABASE="sqlite"
CREATE_VENV=true
INSTALL_DEPS=true
REPO_URL="https://github.com/camcoder337/django-boilerplate.git"

# Parse additional arguments
shift
while [[ $# -gt 0 ]]; do
    case $1 in
        --database)
            DATABASE="$2"
            shift 2
            ;;
        --no-venv)
            CREATE_VENV=false
            shift
            ;;
        --no-deps)
            INSTALL_DEPS=false
            shift
            ;;
        --repo-url)
            REPO_URL="$2"
            shift 2
            ;;
        *)
            print_warning "Unknown option: $1"
            shift
            ;;
    esac
done

echo ""
echo -e "${BOLD}${CYAN}🚀 Django Boilerplate Project Creator${NC}"
echo "====================================="
echo -e "${BLUE}Project: ${PROJECT_NAME}${NC}"
echo -e "${BLUE}Database: ${DATABASE}${NC}"
echo -e "${BLUE}Repository: ${REPO_URL}${NC}"
echo "====================================="
echo ""

TOTAL_STEPS=8
CURRENT_STEP=0

# Step 1: Check system requirements
((CURRENT_STEP++))
print_step $CURRENT_STEP $TOTAL_STEPS "Checking system requirements"

# Check Python version
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    exit 1
fi

python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
min_version="3.9"
if [ "$(printf '%s\n' "$min_version" "$python_version" | sort -V | head -n1)" != "$min_version" ]; then
    print_error "Python 3.9+ is required. Current version: $python_version"
    exit 1
fi

# Check Git
if ! command -v git &> /dev/null; then
    print_error "Git is not installed"
    exit 1
fi

print_success "System requirements check passed"

# Step 2: Check if project directory exists
((CURRENT_STEP++))
print_step $CURRENT_STEP $TOTAL_STEPS "Validating project directory"

if [ -d "$PROJECT_NAME" ]; then
    print_error "Directory '$PROJECT_NAME' already exists!"
    exit 1
fi

print_success "Project directory validation passed"

# Step 3: Clone repository
((CURRENT_STEP++))
print_step $CURRENT_STEP $TOTAL_STEPS "Cloning boilerplate repository"

if ! git clone --depth 1 "$REPO_URL" "$PROJECT_NAME"; then
    print_error "Failed to clone repository"
    exit 1
fi

cd "$PROJECT_NAME"
print_success "Repository cloned successfully"

# Step 4: Clean Git history and initialize new repo
((CURRENT_STEP++))
print_step $CURRENT_STEP $TOTAL_STEPS "Setting up version control"

rm -rf .git
git init > /dev/null 2>&1
print_success "New Git repository initialized"

# Step 5: Create virtual environment
((CURRENT_STEP++))
print_step $CURRENT_STEP $TOTAL_STEPS "Creating virtual environment"

if [ "$CREATE_VENV" = true ]; then
    if ! python3 -m venv venv; then
        print_error "Failed to create virtual environment"
        exit 1
    fi
    print_success "Virtual environment created"
else
    print_info "Skipping virtual environment creation"
fi

# Step 6: Install dependencies
((CURRENT_STEP++))
print_step $CURRENT_STEP $TOTAL_STEPS "Installing dependencies"

if [ "$INSTALL_DEPS" = true ] && [ "$CREATE_VENV" = true ]; then
    source venv/bin/activate

    pip install --upgrade pip > /dev/null

    if ! pip install -r requirements.txt > /dev/null; then
        print_error "Failed to install production dependencies"
        exit 1
    fi

    # Try to install dev dependencies (optional)
    if [ -f "requirements-dev.txt" ]; then
        pip install -r requirements-dev.txt > /dev/null 2>&1 || print_warning "Could not install development dependencies"
    fi

    print_success "Dependencies installed"
else
    print_info "Skipping dependency installation"
fi

# Step 7: Setup environment and Django
((CURRENT_STEP++))
print_step $CURRENT_STEP $TOTAL_STEPS "Configuring Django"

# Create .env file
if [ -f ".env.example" ]; then
    cp .env.example .env
else
    cat > .env << EOF
SECRET_KEY=$(python3 -c 'import secrets; import string; chars = string.ascii_letters + string.digits + "!@#$%^&*(-_=+)"; print("".join(secrets.choice(chars) for _ in range(50)))')
DEBUG=True
DJANGO_SETTINGS_MODULE=core.settings.development
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
LANGUAGE_CODE=en-us
TIME_ZONE=UTC
EOF
fi

# Configure database if PostgreSQL is requested
if [ "$DATABASE" = "postgresql" ]; then
    db_name="${PROJECT_NAME,,}_dev"  # Convert to lowercase
    echo "" >> .env
    echo "# PostgreSQL Configuration" >> .env
    echo "DATABASE_URL=postgresql://postgres:password@localhost:5432/$db_name" >> .env
fi

# Run Django setup if virtual environment was created
if [ "$CREATE_VENV" = true ]; then
    source venv/bin/activate

    python manage.py check > /dev/null 2>&1 || print_warning "Django check failed"
    python manage.py makemigrations > /dev/null 2>&1
    python manage.py migrate > /dev/null 2>&1
    python manage.py collectstatic --noinput > /dev/null 2>&1 || true
fi

print_success "Django configuration completed"

# Step 8: Finalize project
((CURRENT_STEP++))
print_step $CURRENT_STEP $TOTAL_STEPS "Finalizing project"

# Create initial commit
git add . > /dev/null 2>&1
git commit -m "Initial commit from Django Boilerplate" > /dev/null 2>&1

# Create project info file
cat > .project_info.json << EOF
{
  "project_name": "$PROJECT_NAME",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "boilerplate_version": "1.0.0",
  "database": "$DATABASE",
  "python_version": "$python_version"
}
EOF

print_success "Project finalization completed"

# Print success message
echo ""
echo -e "${BOLD}${GREEN}================================================================${NC}"
echo -e "${BOLD}${GREEN}🎉 PROJECT '$PROJECT_NAME' CREATED SUCCESSFULLY!${NC}"
echo -e "${BOLD}${GREEN}================================================================${NC}"
echo ""
echo -e "${BLUE}📁 Project Location: $(pwd)${NC}"
echo ""
echo -e "${YELLOW}${BOLD}📋 Next Steps:${NC}"
echo -e "${CYAN}1. cd $PROJECT_NAME${NC}"
echo -e "${CYAN}2. source venv/bin/activate${NC}"
echo -e "${CYAN}3. python manage.py createsuperuser${NC}"
echo -e "${CYAN}4. python manage.py runserver${NC}"
echo ""
echo -e "${YELLOW}${BOLD}🌐 Your application will be available at:${NC}"
echo -e "${GREEN}   • Frontend: http://127.0.0.1:8000/${NC}"
echo -e "${GREEN}   • API: http://127.0.0.1:8000/api/${NC}"
echo -e "${GREEN}   • Admin: http://127.0.0.1:8000/admin/${NC}"
echo ""

if [ "$DATABASE" = "postgresql" ]; then
    echo -e "${YELLOW}${BOLD}💾 Database Configuration:${NC}"
    echo -e "${YELLOW}   • Don't forget to create your PostgreSQL database${NC}"
    echo -e "${YELLOW}   • Update DATABASE_URL in .env file if needed${NC}"
    echo ""
fi

echo -e "${BLUE}${BOLD}📚 Documentation:${NC}"
echo -e "${BLUE}   • README.md for detailed setup instructions${NC}"
echo -e "${BLUE}   • .env file for environment configuration${NC}"
echo ""
echo -e "${GREEN}${BOLD}🚀 Happy coding with Django Boilerplate!${NC}"
echo ""