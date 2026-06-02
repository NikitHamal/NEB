@echo off
echo ========================================================
echo Starting NEBians Local Django Dev Server
echo ========================================================

if not exist .venv (
    echo Creating Python virtual environment
    py -m venv .venv
)

echo Activating virtual environment
call .venv\Scripts\activate

echo Installing requirements
pip install -r requirements.txt

REM Local development defaults. Override these in your shell or .env as needed.
set DEBUG=True
set SECRET_KEY=django-insecure-local-development-only-change-me
set DB_ENGINE=mysql

echo Migrating database
python manage.py migrate

echo.
echo To create a staff/admin account, run:
echo python manage.py createsuperuser
echo.
echo Site: http://localhost:8000/
echo Custom admin UI: http://localhost:8000/admin/
echo Django admin: http://localhost:8000/admin-django/
echo.
python manage.py runserver
