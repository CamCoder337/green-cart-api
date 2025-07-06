@echo off
REM Django Boilerplate CLI for Windows
REM Usage: create_project.bat <project_name>

setlocal enabledelayedexpansion

REM Check if project name is provided
if "%1"=="" (
    echo ❌ Error: Project name is required
    echo.
    echo Usage: create_project.bat ^<project_name^>
    echo Example: create_project.bat myproject
    pause
    exit /b 1
)

set PROJECT_NAME=%1
set REPO_URL=https://github.com/votre-username/django-boilerplate.git

echo.
echo 🚀 Django Boilerplate Project Creator
echo =====================================
echo Project: %PROJECT_NAME%
echo Repository: %REPO_URL%
echo =====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.9+ and try again
    pause
    exit /b 1
)

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed or not in PATH
    echo Please install Git and try again
    pause
    exit /b 1
)

REM Check if project directory already exists
if exist "%PROJECT_NAME%" (
    echo ❌ Directory '%PROJECT_NAME%' already exists!
    pause
    exit /b 1
)

echo [1/7] 📥 Cloning repository...
git clone --depth 1 %REPO_URL% %PROJECT_NAME%
if errorlevel 1 (
    echo ❌ Failed to clone repository
    pause
    exit /b 1
)

cd %PROJECT_NAME%

echo [2/7] 🧹 Cleaning up Git history...
rmdir /s /q .git >nul 2>&1
git init >nul 2>&1

echo [3/7] 🐍 Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

echo [4/7] ⚙️ Activating virtual environment...
call venv\Scripts\activate.bat

echo [5/7] 📦 Installing dependencies...
python -m pip install --upgrade pip >nul
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

pip install -r requirements-dev.txt >nul 2>&1

echo [6/7] 🔧 Setting up Django...
copy .env.example .env >nul 2>&1

REM Generate a simple secret key
python -c "import secrets; import string; chars = string.ascii_letters + string.digits + '!@#$%%^&*(-_=+)'; key = ''.join(secrets.choice(chars) for _ in range(50)); print('SECRET_KEY=' + key)" > temp_key.txt
for /f "tokens=*" %%i in (temp_key.txt) do set SECRET_KEY=%%i
del temp_key.txt

REM Update .env file
(
echo %SECRET_KEY%
echo DEBUG=True
echo DJANGO_SETTINGS_MODULE=core.settings.development
echo ALLOWED_HOSTS=localhost,127.0.0.1
echo DATABASE_URL=sqlite:///db.sqlite3
echo LANGUAGE_CODE=en-us
echo TIME_ZONE=UTC
) > .env

python manage.py check >nul
python manage.py makemigrations >nul
python manage.py migrate >nul

echo [7/7] 🎯 Finalizing project...
git add . >nul 2>&1
git commit -m "Initial commit from Django Boilerplate" >nul 2>&1

echo.
echo ================================================================
echo 🎉 PROJECT '%PROJECT_NAME%' CREATED SUCCESSFULLY!
echo ================================================================
echo.
echo 📁 Project Location: %cd%
echo.
echo 📋 Next Steps:
echo 1. cd %PROJECT_NAME%
echo 2. venv\Scripts\activate
echo 3. python manage.py createsuperuser
echo 4. python manage.py runserver
echo.
echo 🌐 Your application will be available at:
echo    • Frontend: http://127.0.0.1:8000/
echo    • API: http://127.0.0.1:8000/api/
echo    • Admin: http://127.0.0.1:8000/admin/
echo.
echo 🚀 Happy coding with Django Boilerplate!
echo.
pause