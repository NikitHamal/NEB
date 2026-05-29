# passenger_wsgi.py
# -------------------------------------------------------------------
# This is the cPanel Python Pro / Phusion Passenger entry point.
# -------------------------------------------------------------------
import os
import sys

# Explicitly load your virtualenv site-packages
VENV_PACKAGES = '/home/consicac/virtualenv/nebians_api/3.13/lib/python3.13/site-packages'
if VENV_PACKAGES not in sys.path:
    sys.path.insert(0, VENV_PACKAGES)

# Add your project directory to Python path
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')

from nebians.wsgi import application

