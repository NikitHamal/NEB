import os
import sys
import django
import requests
import json
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
django.setup()

from api.qwen_utils.client import QwenClient
from api.qwen_utils.models import get_default_model
from api import qwen_proxy

print("Starting deep Qwen debug...")
client = QwenClient()
session, headers = client._ensure_session()

print("Session cookies:")
for c in session.cookies:
    print(f"  {c.name}: {c.value[:30]}...")

print("\nSession headers:")
for h, v in session.headers.items():
    print(f"  {h}: {v}")

model = get_default_model()
payload = {
    "title": "New Chat",
    "models": [model],
    "chat_mode": "normal",
    "chat_type": "t2t",
    "timestamp": int(time.time() * 1000),
}
print(f"\nSending chat creation request with payload: {payload}")
try:
    resp = session.post(f"{qwen_proxy.QWEN_URL}/api/v2/chats/new", json=payload, timeout=30)
    print(f"Response Status Code: {resp.status_code}")
    print("Response Headers:")
    for h, v in resp.headers.items():
         print(f"  {h}: {v}")
    print("\nResponse Body:")
    print(resp.text[:2000])
except Exception as e:
    print(f"Exception during request: {e}")
