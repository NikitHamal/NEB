"""Seed forum posts and mint a logged-in session for design audits (DEBUG + sqlite only).
   cd backend_python && DB_ENGINE=sqlite DEBUG=True SECRET_KEY=x python3 ../tools/design/seed_demo.py
Prints the session id; pass it to audit.mjs with --cookie."""
import os, sys, time, uuid
sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
import django
django.setup()
from django.conf import settings
assert settings.DEBUG
from django.contrib.sessions.backends.db import SessionStore
from api.models import User, Post, Reply
from api.security import issue_auth_token
from api.serializers import UserSerializer
from web.view_helpers import _normalize_user_data

now = int(time.time() * 1000)
users = list(User.objects.all())
if not Post.objects.exists():
    rows = [
        ('Why is the second ionisation energy always higher?', 'Once one electron is gone the rest are held more tightly. Is that the whole reason or is there more to it?', 'Chemistry'),
        ('Best way to revise Class 12 Physics in 3 weeks?', 'Board exams are close. Which chapters carry the most marks, and how do I plan the days?', 'Physics'),
        ('Integration by parts, when do I pick u?', 'LIATE helps but I still get stuck on products of two functions.', 'Mathematics'),
        ('Share your Computer Science project ideas', 'Looking for simple project ideas for the practical exam.', 'Computer Science'),
    ]
    for i, (t, c, cat) in enumerate(rows):
        u = users[i % len(users)]
        p = Post.objects.create(id=str(uuid.uuid4()), user=u, title=t, content=c, category=cat, thumbs_up_count=3 + i * 4, reply_count=2, view_count=40 + i * 30, created_at=now - i * 3600000)
        for j in range(2):
            Reply.objects.create(id=str(uuid.uuid4()), post=p, user=users[(i + j + 1) % len(users)], content='Think of it as effective nuclear charge: fewer electrons, same pull.', thumbs_up_count=j, created_at=now - i * 3600000 + (j + 1) * 60000)
u = User.objects.get(username='student_demo')
tok = issue_auth_token(u)
s = SessionStore()
s['auth_token'] = tok
s['user_data'] = _normalize_user_data(UserSerializer(u).data)
s.save()
print(s.session_key)
