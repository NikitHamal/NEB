"""Mint a fresh bx-umidtoken for the qwencloud proxy.

Each risk token is good for roughly ~20 chat turns (the gateway reports
``xUmidNumber``/``limit`` via ``qwencloud_proxy.quota()``). When turns start
failing with a quota-exhausted error:

1. Run this script on a machine WITH a browser (needs Playwright Chromium):
       python tools/mint_qwencloud_token.py
2. Copy the printed token into the server ``.env`` as QWENCLOUD_UMIDTOKEN.
3. Restart the web process (touch tmp/restart.txt) and the background worker.

The script loads the public try-ai page headlessly, waits for the risk SDK to
attach its headers, and prints the ``bx-umidtoken`` it observes.
"""
import sys

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("playwright is not installed: pip install playwright && playwright install chromium")

found = {}


def on_req(req):
    token = req.headers.get("bx-umidtoken")
    if token and "token" not in found:
        found["token"] = token


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.on("request", on_req)
    page.goto("https://www.qwencloud.com/try-ai?scene=chat", timeout=60000)
    page.wait_for_timeout(12000)
    browser.close()

if "token" in found:
    print(found["token"])
else:
    sys.exit("no bx-umidtoken observed; the page may have changed, retry once")
