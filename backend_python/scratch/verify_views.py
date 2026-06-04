import os
import sys
import django
from django.test import Client
from django.db import transaction

# Setup django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
django.setup()

from django.conf import settings
# Allow testserver in ALLOWED_HOSTS for testing
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS = list(settings.ALLOWED_HOSTS) + ['testserver']

from api.models import User, Resource, ArenaChatSession
from api.security import issue_auth_token

def test_routes():
    print("=== STARTING INTEGRATION TESTS ===")
    
    # 1. Initialize client and create/get test user
    client = Client()
    
    user = User.objects.filter(username='test_verify_user').first()
    if not user:
        # Create a test user
        user = User.objects.create(
            id='verify-user-id-123',
            username='test_verify_user',
            email='verify@nebians.com',
            display_name='Verify User',
            email_verified=True,
            created_at=0
        )
        print("Created test user: test_verify_user")
    
    # Generate session token and set in client session
    token = issue_auth_token(user)
    session = client.session
    session['auth_token'] = token
    # Also set the expected user_data in the session
    session['user_data'] = {
        'id': user.id,
        'username': user.username,
        'display_name': user.display_name,
        'email': user.email,
        'photo_url': user.photo_url or '',
        'class_level': 'Class 12',
        'gender': 'Male'
    }
    session.save()
    print(f"Issued auth token and set in test session.")

    # 2. Test Library page
    print("\nTesting Library landing page (/library/)...")
    res = client.get('/library/')
    if res.status_code == 200:
        print("[OK] Library page load successful (200 OK)")
        html = res.content.decode('utf-8')
        if 'Digital Library' in html:
            print("[OK] 'Digital Library' tab is visible in HTML")
        else:
            print("[FAIL] 'Digital Library' tab is missing in HTML")
    else:
        print(f"[FAIL] Library page failed with status {res.status_code}")

    print("\nTesting Library Categories tab (/library/?tab=categories)...")
    res = client.get('/library/?tab=categories')
    if res.status_code == 200:
        print("[OK] Categories page load successful (200 OK)")
        html = res.content.decode('utf-8')
        if 'Syllabus' in html:
            print("[OK] 'Syllabus' tab is active in HTML")
        else:
            print("[FAIL] 'Syllabus' tab is missing in HTML")
            
        if 'Class 12' in html:
            print("[OK] Class 12 accordion header is visible in HTML")
        else:
            print("[FAIL] Class 12 accordion header is missing in HTML")
    else:
        print(f"[FAIL] Categories page failed with status {res.status_code}")

    # 3. Test Subject pages
    subject_pages = [
        ('/subject/class-12/english/', 'Class 12 English', ['The Bull', 'The Selfish Giant']),
        ('/subject/class-12/computer-science/', 'Class 12 Computer Science', ['Database Management System', 'Computer Network']),
        ('/subject/class-11/physics/', 'Class 11 Physics', ['Mechanics', 'Thermodynamics']),
    ]
    
    for url, label, expected_keywords in subject_pages:
        print(f"\nTesting Subject page: {label} ({url})...")
        res = client.get(url)
        if res.status_code == 200:
            print(f"[OK] {label} page load successful (200 OK)")
            html = res.content.decode('utf-8')
            
            # Check title
            if label in html:
                print(f"[OK] Page title contains '{label}'")
            else:
                print(f"[FAIL] Page title is incorrect")
                
            # Check expected seeded chapters / resources
            for kw in expected_keywords:
                if kw in html:
                    print(f"[OK] Found chapter/resource name: '{kw}'")
                else:
                    print(f"[FAIL] Chapter/resource name '{kw}' not found in page")
                    
            if label == 'Class 12 English':
                if 'Chapter Guide' in html and 'Oscar Wilde' in html:
                    print("[OK] Seeded text syllabus content is visible on Class 12 English page")
                else:
                    print("[FAIL] Seeded text syllabus content is missing on Class 12 English page")

            if 'Neby AI helper' in html:
                print("[OK] Neby AI tab is present on the page")
            else:
                print("[FAIL] Neby AI tab is missing")
        else:
            print(f"[FAIL] {label} page failed with status {res.status_code}")

    # 4. Test Neby AI AJAX session list
    print("\nTesting Neby AI session list AJAX endpoint (/ajax/neby-arena/sessions/)...")
    res = client.get('/ajax/neby-arena/sessions/')
    if res.status_code == 200:
        print("[OK] Session list AJAX endpoint successful (200 OK)")
        data = res.json()
        print(f"[OK] Received session list payload: {data}")
    else:
        print(f"[FAIL] Session list AJAX failed with status {res.status_code}")

    print("\n=== TESTS COMPLETED ===")

if __name__ == '__main__':
    test_routes()
