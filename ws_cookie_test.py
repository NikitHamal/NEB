#!/usr/bin/env python3
"""
Test: WebSocket with session cookie to compare behavior.
"""
import json
import websocket

# Read cookies
cookies = ""
with open(r"F:\NEB\cookies_fresh.txt", "r") as f:
    for line in f:
        if line.startswith("#") or not line.strip():
            continue
        parts = line.strip().split("\t")
        if len(parts) >= 7:
            cookies += f"{parts[5]}={parts[6]}; "
cookies = cookies.strip("; ")

print(f"Using cookies: {cookies[:100]}")

WS_URL = "wss://towers-pest-kelly-skins.trycloudflare.com/ws/"

# With cookie
ws = websocket.create_connection(
    WS_URL,
    origin="https://nebians.consica.com.np",
    cookie=cookies,
    timeout=10
)
ready = ws.recv()
print(f"\nWith cookie - Ready: {ready}")

# Now check what user_id is shown
data = json.loads(ready)
if data.get("user_id"):
    print(f"[!] Authenticated WebSocket - user_id: {data['user_id']}")
else:
    print(f"[!] WebSocket does NOT recognize session cookie - user_id: null")
    print(f"    This means WebSocket auth doesn't use session cookies")

ws.close()

# Also test with auth header
ws = websocket.create_connection(
    WS_URL,
    origin="https://nebians.consica.com.np",
    header=["Authorization: Bearer fake_token"],
    timeout=10
)
ready = ws.recv()
print(f"\nWith auth header - Ready: {ready}")
data = json.loads(ready)
if data.get("user_id"):
    print(f"[!] Authenticated WebSocket - user_id: {data['user_id']}")
else:
    print(f"[!] WebSocket doesn't accept Authorization header either - user_id: null")

ws.close()
