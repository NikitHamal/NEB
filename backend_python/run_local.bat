@echo off
echo ========================================================
echo Starting NEBians Local Django Dev Server
echo ========================================================

REM Check if virtualenv directory exists
if not exist .venv (
    echo Creating Python 3.13 virtual environment
    py -3.13 -m venv .venv
)

REM Activate virtualenv
echo Activating virtual environment
call .venv\Scripts\activate

REM Install dependencies
echo Installing requirements
pip install -r requirements.txt

REM Run database migrations on local SQLite
echo Migrating database local db
python manage.py migrate

REM Start Django development server with auto-reload
echo Starting server
echo Access the site at http://localhost:8000/
echo Access the Admin Panel at http://localhost:8000/admin/
echo Admin credentials are admin and admin123
python manage.py runserver
