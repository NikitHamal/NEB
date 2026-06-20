#!/usr/bin/env python3
"""Test WebSocket security on nebians.consica.com.np"""
import json
import sys

# Try to use websocket-client or fall back to a raw socket
try:
    import websocket
except ImportError:
    print("Installing websocket-client...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "websocket-client", "-q"])
    import websocket


def test_ws():
    ws_url = "wss://towers-pest-kelly-skins.trycloudflare.com/ws/"
    print(f"[*] Connecting to {ws_url}")

    ws = websocket.create_connection(
        ws_url,
        origin="https://nebians.consica.com.np",
        timeout=10,
        host="towers-pest-kelly-skins.trycloudflare.com",
    )

    # Read the ready message
    ready = ws.recv()
    print(f"[READY] {ready}")

    # Try subscribing to various channels
    channels = [
        "forum.public",
        "user",
        "post.b5833249-6585-4caa-84fa-a0d599f0cfc5",  # the welcome post
        "post.test",
        "admin",  # try to access admin channel
        "user.testuser",
        "user.d0cfb9b0-d569-49f4-9f37-8383eccd5ff6",  # test user
        "user.dcfb9b0-d569-49f4-9f37-8383eccd5ff6",  # admin user
        "user",  # without ID
        "system",
        "metrics",
    ]

    for ch in channels:
        print(f"\n[*] Subscribing to: {ch}")
        ws.send(json.dumps({"action": "subscribe", "channel": ch}))

        try:
            # Wait for response or timeout
            ws.settimeout(2)
            while True:
                try:
                    msg = ws.recv()
                    print(f"  [RECV] {msg}")
                    if "subscribed" in msg or "error" in msg:
                        break
                except Exception as e:
                    print(f"  [TIMEOUT/ERR] {e}")
                    break
        except Exception as e:
            print(f"  [ERR] {e}")

    # Try sending actions
    print("\n[*] Trying various actions")
    actions = [
        {"action": "ping"},
        {"action": "publish", "channel": "forum.public", "event": "post.created", "data": {"test": 1}},
        {"action": "broadcast", "message": "test"},
        {"action": "admin_command", "command": "list_users"},
        {"action": "get_user", "user_id": "d0cfb9b0-d569-49f4-9f37-8383eccd5ff6"},
    ]

    for a in actions:
        print(f"\n[*] Sending: {a}")
        ws.send(json.dumps(a))
        try:
            ws.settimeout(2)
            msg = ws.recv()
            print(f"  [RECV] {msg}")
        except Exception as e:
            print(f"  [ERR] {e}")

    ws.close()


if __name__ == "__main__":
    test_ws()
