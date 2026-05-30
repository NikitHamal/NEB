import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
django.setup()

from django.conf import settings
from django.contrib.sessions.models import Session

print("--- Django Session Settings ---")
print(f"SESSION_COOKIE_NAME: {settings.SESSION_COOKIE_NAME}")
print(f"SESSION_COOKIE_AGE: {settings.SESSION_COOKIE_AGE}")
print(f"SESSION_COOKIE_SECURE: {getattr(settings, 'SESSION_COOKIE_SECURE', False)}")
print(f"SESSION_COOKIE_SAMESITE: {getattr(settings, 'SESSION_COOKIE_SAMESITE', 'Lax')}")
print(f"SESSION_ENGINE: {settings.SESSION_ENGINE}")
print(f"SESSION_SAVE_EVERY_REQUEST: {settings.SESSION_SAVE_EVERY_REQUEST}")
print(f"DEBUG: {settings.DEBUG}")

print("\n--- Session Database Status ---")
try:
    session_count = Session.objects.count()
    print(f"Total active database sessions: {session_count}")
    if session_count > 0:
        latest = Session.objects.order_by('-expire_date').first()
        print(f"Latest session expires at: {latest.expire_date}")
except Exception as e:
    print(f"ERROR querying sessions table: {e}")
