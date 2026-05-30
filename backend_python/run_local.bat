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

REM Start SSH tunnel for MySQL (port 3307 -> remote 3306)
echo Starting SSH tunnel for MySQL...
start /B ssh -i "%TEMP%\nebians_deploy_key" -o StrictHostKeyChecking=no -o UserKnownHostsFile=NUL -L 3307:localhost:3306 -N consicac@192.250.235.158
timeout /t 3 /nobreak >nul

REM Run database migrations
echo Migrating database
python manage.py migrate

REM Start Django development server with auto-reload
echo Starting server
echo Access the site at http://localhost:8000/
echo Access the Admin Panel at http://localhost:8000/admin/
echo Admin credentials are admin and admin123
python manage.py runserver