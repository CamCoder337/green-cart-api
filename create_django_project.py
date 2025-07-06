#!/usr/bin/env python3
"""
Django Boilerplate CLI - Create a new Django project from boilerplate
Usage: python create_django_project.py <project_name> [options]
"""

import os
import sys
import subprocess
import argparse
import secrets
import string
import shutil
import json
from pathlib import Path
from datetime import datetime


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_colored(message, color=Colors.ENDC):
    """Print colored message to terminal."""
    print(f"{color}{message}{Colors.ENDC}")


def print_step(step_num, total_steps, message):
    """Print step progress."""
    print_colored(f"\n[{step_num}/{total_steps}] {message}", Colors.CYAN)


def print_success(message):
    """Print success message."""
    print_colored(f"✅ {message}", Colors.GREEN)


def print_error(message):
    """Print error message."""
    print_colored(f"❌ {message}", Colors.RED)


def print_warning(message):
    """Print warning message."""
    print_colored(f"⚠️ {message}", Colors.YELLOW)


def print_info(message):
    """Print info message."""
    print_colored(f"ℹ️ {message}", Colors.BLUE)


def generate_secret_key(length=50):
    """Generate a secure Django secret key."""
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print_error("Python 3.9+ is required. Please upgrade your Python version.")
        return False
    return True


def check_git_installed():
    """Check if Git is installed."""
    try:
        subprocess.run(['git', '--version'],
                      capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error("Git is not installed. Please install Git first.")
        return False


def clone_repository(repo_url, project_name, branch='main'):
    """Clone the boilerplate repository."""
    try:
        print_info(f"Cloning from {repo_url}")
        subprocess.run([
            'git', 'clone',
            '--branch', branch,
            '--single-branch',
            '--depth', '1',
            repo_url,
            project_name
        ], check=True)
        print_success("Repository cloned successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to clone repository: {e}")
        return False


def setup_environment_file(project_path, project_name, settings):
    """Create and configure the .env file."""
    env_example_path = project_path / '.env.example'
    env_path = project_path / '.env'

    if not env_example_path.exists():
        print_warning(".env.example not found, creating basic .env file")
        env_content = f"""# Django Boilerplate Environment Configuration
SECRET_KEY={generate_secret_key()}
DEBUG=True
DJANGO_SETTINGS_MODULE=core.settings.development
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
LANGUAGE_CODE=en-us
TIME_ZONE=UTC
"""
    else:
        with open(env_example_path, 'r', encoding='utf-8') as f:
            env_content = f.read()

        # Replace default values
        secret_key = generate_secret_key()
        env_content = env_content.replace('your-secret-key-here', secret_key)
        env_content = env_content.replace('django-boilerplate', project_name.lower())

    # Apply custom settings
    if settings.get('database') == 'postgresql':
        db_name = f"{project_name.lower()}_dev"
        env_content += f"\n# PostgreSQL Configuration\nDATABASE_URL=postgresql://postgres:password@localhost:5432/{db_name}\n"

    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(env_content)

    print_success(".env file created with generated secret key")


def clean_git_history(project_path):
    """Remove original git history and initialize new repository."""
    git_path = project_path / '.git'
    if git_path.exists():
        shutil.rmtree(git_path)
        print_success("Original Git history removed")

    try:
        subprocess.run(['git', 'init'], cwd=project_path, check=True)
        print_success("New Git repository initialized")
        return True
    except subprocess.CalledProcessError:
        print_warning("Could not initialize Git repository")
        return False


def create_virtual_environment(project_path, python_version='python3'):
    """Create Python virtual environment."""
    venv_path = project_path / 'venv'

    try:
        print_info(f"Creating virtual environment with {python_version}")
        subprocess.run([
            python_version, '-m', 'venv', str(venv_path)
        ], check=True)
        print_success(f"Virtual environment created at {venv_path}")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to create virtual environment: {e}")
        return False


def get_pip_path(project_path):
    """Get the path to pip in the virtual environment."""
    if os.name == 'nt':  # Windows
        return project_path / 'venv' / 'Scripts' / 'pip'
    else:  # Unix/Linux/macOS
        return project_path / 'venv' / 'bin' / 'pip'


def get_python_path(project_path):
    """Get the path to Python in the virtual environment."""
    if os.name == 'nt':  # Windows
        return project_path / 'venv' / 'Scripts' / 'python'
    else:  # Unix/Linux/macOS
        return project_path / 'venv' / 'bin' / 'python'


def install_dependencies(project_path, dev_dependencies=True):
    """Install project dependencies."""
    pip_path = get_pip_path(project_path)

    # Upgrade pip first
    try:
        subprocess.run([
            str(pip_path), 'install', '--upgrade', 'pip'
        ], cwd=project_path, check=True)
    except subprocess.CalledProcessError:
        print_warning("Could not upgrade pip")

    # Install production dependencies
    requirements_file = 'requirements.txt'
    if (project_path / requirements_file).exists():
        try:
            print_info("Installing production dependencies...")
            subprocess.run([
                str(pip_path), 'install', '-r', requirements_file
            ], cwd=project_path, check=True)
            print_success("Production dependencies installed")
        except subprocess.CalledProcessError as e:
            print_error(f"Failed to install production dependencies: {e}")
            return False

    # Install development dependencies if requested
    if dev_dependencies:
        dev_requirements_file = 'requirements-dev.txt'
        if (project_path / dev_requirements_file).exists():
            try:
                print_info("Installing development dependencies...")
                subprocess.run([
                    str(pip_path), 'install', '-r', dev_requirements_file
                ], cwd=project_path, check=True)
                print_success("Development dependencies installed")
            except subprocess.CalledProcessError as e:
                print_warning(f"Could not install development dependencies: {e}")

    return True


def run_django_setup(project_path):
    """Run Django setup commands."""
    python_path = get_python_path(project_path)

    commands = [
        (['python', 'manage.py', 'check'], "Django configuration check"),
        (['python', 'manage.py', 'makemigrations'], "Creating migrations"),
        (['python', 'manage.py', 'migrate'], "Applying migrations"),
        (['python', 'manage.py', 'collectstatic', '--noinput'], "Collecting static files"),
    ]

    for command, description in commands:
        try:
            print_info(description)
            # Use the virtual environment Python
            command[0] = str(python_path)
            subprocess.run(command, cwd=project_path, check=True)
            print_success(f"{description} completed")
        except subprocess.CalledProcessError as e:
            if 'collectstatic' in command:
                print_warning(f"Static files collection failed (this is normal if DEBUG=True)")
            else:
                print_error(f"{description} failed: {e}")
                return False

    return True


def create_project_info(project_path, project_name, settings):
    """Create project information file."""
    info = {
        'project_name': project_name,
        'created_at': datetime.now().isoformat(),
        'boilerplate_version': '1.0.0',
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'settings': settings,
        'next_steps': [
            f"cd {project_name}",
            "source venv/bin/activate  # or venv\\Scripts\\activate on Windows",
            "python manage.py createsuperuser",
            "python manage.py runserver"
        ]
    }

    info_path = project_path / '.project_info.json'
    with open(info_path, 'w', encoding='utf-8') as f:
        json.dump(info, f, indent=2)


def print_success_message(project_name, project_path, settings):
    """Print final success message with instructions."""
    print_colored("\n" + "="*60, Colors.GREEN)
    print_colored(f"🎉 PROJECT '{project_name.upper()}' CREATED SUCCESSFULLY!", Colors.GREEN + Colors.BOLD)
    print_colored("="*60, Colors.GREEN)

    print_colored(f"\n📁 Project Location: {project_path}", Colors.BLUE)

    print_colored(f"\n📋 Next Steps:", Colors.YELLOW + Colors.BOLD)
    print(f"1. {Colors.CYAN}cd {project_name}{Colors.ENDC}")

    if os.name == 'nt':  # Windows
        print(f"2. {Colors.CYAN}venv\\Scripts\\activate{Colors.ENDC}")
    else:  # Unix/Linux/macOS
        print(f"2. {Colors.CYAN}source venv/bin/activate{Colors.ENDC}")

    print(f"3. {Colors.CYAN}python manage.py createsuperuser{Colors.ENDC}")
    print(f"4. {Colors.CYAN}python manage.py runserver{Colors.ENDC}")

    print_colored(f"\n🌐 Your application will be available at:", Colors.YELLOW + Colors.BOLD)
    print_colored("   • Frontend: http://127.0.0.1:8000/", Colors.GREEN)
    print_colored("   • API: http://127.0.0.1:8000/api/", Colors.GREEN)
    print_colored("   • Admin: http://127.0.0.1:8000/admin/", Colors.GREEN)

    if settings.get('database') == 'postgresql':
        print_colored(f"\n💾 Database Configuration:", Colors.YELLOW + Colors.BOLD)
        print_colored("   • Don't forget to create your PostgreSQL database", Colors.YELLOW)
        print_colored(f"   • Update DATABASE_URL in .env file", Colors.YELLOW)

    print_colored(f"\n📚 Documentation:", Colors.BLUE + Colors.BOLD)
    print_colored("   • README.md for detailed setup instructions", Colors.BLUE)
    print_colored("   • .env.example for environment configuration", Colors.BLUE)

    print_colored(f"\n🚀 Happy coding with Django Boilerplate!", Colors.GREEN + Colors.BOLD)


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Create a new Django project from boilerplate",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python create_django_project.py myproject
  python create_django_project.py myproject --database postgresql
  python create_django_project.py myproject --repo-url https://github.com/user/repo.git
  python create_django_project.py myproject --no-venv --no-deps
        """
    )

    parser.add_argument(
        'project_name',
        help='Name of the Django project to create'
    )

    parser.add_argument(
        '--repo-url',
        default='https://github.com/votre-username/django-boilerplate.git',
        help='URL of the boilerplate repository'
    )

    parser.add_argument(
        '--branch',
        default='main',
        help='Branch to clone (default: main)'
    )

    parser.add_argument(
        '--database',
        choices=['sqlite', 'postgresql'],
        default='sqlite',
        help='Database type to configure (default: sqlite)'
    )

    parser.add_argument(
        '--python-version',
        default='python3',
        help='Python version to use for virtual environment (default: python3)'
    )

    parser.add_argument(
        '--no-venv',
        action='store_true',
        help='Skip virtual environment creation'
    )

    parser.add_argument(
        '--no-deps',
        action='store_true',
        help='Skip dependency installation'
    )

    parser.add_argument(
        '--no-dev-deps',
        action='store_true',
        help='Skip development dependencies installation'
    )

    parser.add_argument(
        '--no-git',
        action='store_true',
        help='Skip Git repository initialization'
    )

    args = parser.parse_args()

    # Validate project name
    project_name = args.project_name
    if not project_name.replace('_', '').replace('-', '').isalnum():
        print_error("Project name must contain only letters, numbers, hyphens, and underscores.")
        sys.exit(1)

    project_path = Path(project_name).resolve()

    # Check if project directory already exists
    if project_path.exists():
        print_error(f"Directory '{project_name}' already exists!")
        sys.exit(1)

    # Store settings
    settings = {
        'database': args.database,
        'python_version': args.python_version,
        'include_dev_deps': not args.no_dev_deps,
        'repo_url': args.repo_url,
        'branch': args.branch
    }

    # Print header
    print_colored("\n🚀 DJANGO BOILERPLATE PROJECT CREATOR", Colors.HEADER + Colors.BOLD)
    print_colored("="*50, Colors.HEADER)
    print_colored(f"Project: {project_name}", Colors.BLUE)
    print_colored(f"Location: {project_path}", Colors.BLUE)
    print_colored(f"Repository: {args.repo_url}", Colors.BLUE)
    print_colored(f"Database: {args.database}", Colors.BLUE)
    print_colored("="*50, Colors.HEADER)

    total_steps = 8
    current_step = 0

    # Step 1: Check system requirements
    current_step += 1
    print_step(current_step, total_steps, "Checking system requirements")

    if not check_python_version():
        sys.exit(1)

    if not args.no_git and not check_git_installed():
        sys.exit(1)

    print_success("System requirements check passed")

    # Step 2: Clone repository
    current_step += 1
    print_step(current_step, total_steps, "Cloning boilerplate repository")

    if not clone_repository(args.repo_url, project_name, args.branch):
        sys.exit(1)

    # Step 3: Setup environment configuration
    current_step += 1
    print_step(current_step, total_steps, "Configuring environment")

    setup_environment_file(project_path, project_name, settings)

    # Step 4: Clean Git history
    current_step += 1
    print_step(current_step, total_steps, "Setting up version control")

    if not args.no_git:
        clean_git_history(project_path)

    # Step 5: Create virtual environment
    current_step += 1
    print_step(current_step, total_steps, "Creating virtual environment")

    if not args.no_venv:
        if not create_virtual_environment(project_path, args.python_version):
            sys.exit(1)
    else:
        print_info("Skipping virtual environment creation")

    # Step 6: Install dependencies
    current_step += 1
    print_step(current_step, total_steps, "Installing dependencies")

    if not args.no_deps and not args.no_venv:
        if not install_dependencies(project_path, not args.no_dev_deps):
            sys.exit(1)
    else:
        print_info("Skipping dependency installation")

    # Step 7: Run Django setup
    current_step += 1
    print_step(current_step, total_steps, "Setting up Django")

    if not args.no_venv:
        if not run_django_setup(project_path):
            print_warning("Django setup had some issues, but project was created")
    else:
        print_info("Skipping Django setup (no virtual environment)")

    # Step 8: Finalize project
    current_step += 1
    print_step(current_step, total_steps, "Finalizing project")

    create_project_info(project_path, project_name, settings)

    # Final commit if Git is enabled
    if not args.no_git:
        try:
            subprocess.run(['git', 'add', '.'], cwd=project_path, check=True)
            subprocess.run(['git', 'commit', '-m', 'Initial commit from Django Boilerplate'],
                         cwd=project_path, check=True)
            print_success("Initial Git commit created")
        except subprocess.CalledProcessError:
            print_warning("Could not create initial Git commit")

    print_success("Project finalization completed")

    # Print success message
    print_success_message(project_name, project_path, settings)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\n❌ Project creation cancelled by user.", Colors.RED)
        sys.exit(1)
    except Exception as e:
        print_colored(f"\n\n❌ Unexpected error: {e}", Colors.RED)
        sys.exit(1)