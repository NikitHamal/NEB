#!/usr/bin/env python3
"""Plays the *browser* half of the desktop sign-in for the live end-to-end test.

usage: e2e-handoff.py <base-url> <existing-bearer-token-of-a-test-user>
Waits for the desktop client to write its login URL to /tmp/handoff_url, then:
  1. opens it with no session  -> must bounce to the web login (checks the redirect)
  2. signs in through the site's own /auth/token-login/ (what a finished Google/GitHub login leaves behind)
  3. loads the consent page, extracts the CSRF token and presses Allow.
"""
import os, re, sys, time
import requests

base, token = sys.argv[1].rstrip('/'), sys.argv[2]
for _ in range(600):
    if os.path.exists('/tmp/handoff_url'):
        break
    time.sleep(0.5)
url = open('/tmp/handoff_url').read().strip()
state = url.split('state=')[1]
s = requests.Session()
r = s.get(url, allow_redirects=False)
assert r.status_code == 302 and '/login/?next=' in r['Location'] if False else r.status_code == 302 and '/login/?next=' in r.headers['Location'], r.headers
print('signed-out visitor is sent to login:', r.headers['Location'][:60], '...')
r = s.get(f'{base}/auth/token-login/', params={'token': token, 'next': f'/desktop-auth/?state={state}'})
assert r.status_code == 200 and 'Sign in to NEBians Desktop?' in r.text, r.text[:300]
assert 'e2e_tester' in r.text
csrf = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', r.text).group(1)
r = s.post(f'{base}/desktop-auth/', data={'state': state, 'decision': 'allow', 'csrfmiddlewaretoken': csrf}, headers={'Referer': f'{base}/desktop-auth/'})
assert r.status_code == 200 and "You're signed in" in r.text, r.text[:300]
print('consent page approved')
