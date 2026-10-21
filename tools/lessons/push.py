#!/usr/bin/env python3
"""Push a working tree to the NEB GitHub repo through the AgentSky connector.

`git push` cannot be used from an agent pod on this repo: the only credential
GitHub hands out is the short-lived `temp_clone_token`, and that one is
read-only.  The AgentSky GitHub connector *can* write (the owner's OAuth is
injected server-side), but `actl connector call --body …` passes the body as a
command-line argument, so the kernel's ARG_MAX (~2 MB) caps the payload and a
25 MB PDF cannot be sent.  The connector's HTTP endpoint itself has no such
limit; the only ceiling observed is a ~27 MB blob body (HTTP 413 above that).

So this script talks to the connector endpoint directly:

    POST {ACTL_BASE_URL}/api/agent/connector
    Authorization: Bearer $ACTL_AUTH_TOKEN
    {"app": "github", "method": …, "url": …, "body": …}

and drives the Git Data API (blob -> tree -> commit -> update ref).

Usage
-----
    # sanity check: print the branch head this would build on
    python3 notes/tools/push_branch.py head

    # push the files that changed, in one commit
    python3 notes/tools/push_branch.py push "message" file1 file2 …   # repo-relative
    python3 notes/tools/push_branch.py push "message" --all-changed   # git status

    # delete paths in the same commit
    python3 notes/tools/push_branch.py push "message" --all-changed --delete old.md

Environment: ACTL_BASE_URL, ACTL_AUTH_TOKEN (both provided by the platform),
optionally NEB_REPO ("owner/name") and NEB_BRANCH.
"""
import base64
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

BASE = os.environ["ACTL_BASE_URL"].rstrip("/")
TOKEN = os.environ["ACTL_AUTH_TOKEN"]
REPO = os.environ.get("NEB_REPO", "NikitHamal/NEB")
BRANCH = os.environ.get("NEB_BRANCH", "videos/explainers")
MAX_BLOB = 25 * 1024 * 1024      # stay clear of the connector's 413 ceiling


def _gh_once(method, path, body=None, retries=6, timeout=900):
    url = path if path.startswith("http") else "https://api.github.com" + path
    payload = {"app": "github", "method": method, "url": url}
    if body is not None:
        payload["body"] = json.dumps(body)
    data = json.dumps(payload).encode("utf-8")
    for attempt in range(retries):
        req = urllib.request.Request(
            BASE + "/api/agent/connector", data=data,
            headers={"Authorization": "Bearer " + TOKEN,
                     "Content-Type": "application/json"},
            method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8", "replace")
            break
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", "replace")
            if exc.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(3 * (attempt + 1))
                continue
            if exc.code == 403 and "rate limit" in raw and attempt < retries - 1:
                time.sleep(60 * (attempt + 1))
                continue
            raise SystemExit("github %s %s -> HTTP %s %s"
                             % (method, url, exc.code, raw[:300]))
        except Exception as exc:                      # noqa: BLE001
            if attempt < retries - 1:
                time.sleep(3 * (attempt + 1))
                continue
            raise SystemExit("github %s %s -> %s" % (method, url, exc))
    parsed = json.loads(raw)
    status, inner = parsed.get("status"), parsed.get("body")
    if isinstance(inner, str):
        try:
            inner = json.loads(inner)
        except ValueError:
            pass
    if isinstance(status, int) and status >= 400:
        raise SystemExit("github %s %s -> HTTP %s %s"
                         % (method, url, status, str(inner)[:300]))
    return inner


def gh(method, path, body=None):
    for attempt in range(8):
        try:
            return _gh_once(method, path, body)
        except SystemExit as exc:
            if "rate limit" not in str(exc) or attempt == 7:
                raise
            time.sleep(60 + 30 * attempt)


def api(suffix):
    return "https://api.github.com/repos/%s%s" % (REPO, suffix)


def head_sha():
    return gh("GET", api("/git/ref/heads/" + BRANCH))["object"]["sha"]


def changed_files(root="."):
    out = subprocess.run(["git", "status", "--porcelain"], cwd=root,
                         capture_output=True, text=True, check=True).stdout
    files = []
    for line in out.splitlines():
        code, path = line[:2], line[3:].strip()
        if code.strip() in ("D", "AD"):
            continue
        files.append(path)
    return files


def repo_prefix(root):
    """Repo-relative prefix of the local working tree."""
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=root,
                         capture_output=True, text=True, check=True).stdout.strip()
    return os.path.relpath(os.path.abspath(root), top).replace(os.sep, "/")


def push(paths, message, deletes=(), root=".", progress=True):
    prefix = repo_prefix(root)
    entries = []

    def upload(path):
        local = os.path.join(root, path) if not os.path.isabs(path) else path
        if not os.path.isfile(local):
            raise SystemExit("not a file: %s" % local)
        size = os.path.getsize(local)
        if size > MAX_BLOB:
            raise SystemExit("%s is %.1f MB — over the 25 MB blob ceiling; "
                             "shrink it before pushing" % (path, size / 1e6))
        with open(local, "rb") as fh:
            blob = base64.b64encode(fh.read()).decode("ascii")
        sha = gh("POST", api("/git/blobs"),
                 {"content": blob, "encoding": "base64"})["sha"]
        repo_path = path if prefix in ("", ".") else "%s/%s" % (prefix, path)
        if progress:
            print("  + %-58s %7.2f MB" % (repo_path, size / 1e6), flush=True)
        return {"path": repo_path, "mode": "100644", "type": "blob", "sha": sha}

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=int(os.environ.get("PUSH_WORKERS", "3"))) as ex:
        entries.extend(ex.map(upload, sorted(paths)))
    for path in deletes:
        repo_path = path if prefix in ("", ".") else "%s/%s" % (prefix, path)
        entries.append({"path": repo_path, "mode": "100644", "type": "blob",
                        "sha": None})
        if progress:
            print("  - %s" % repo_path, flush=True)
    if not entries:
        print("nothing to push")
        return None
    base = head_sha()
    tree = base
    for i in range(0, len(entries), 60):            # big trees time out server-side
        tree = gh("POST", api("/git/trees"),
                  {"base_tree": tree, "tree": entries[i:i + 60]})["sha"]
    commit = gh("POST", api("/git/commits"),
                {"message": message, "tree": tree, "parents": [base]})["sha"]
    gh("PATCH", api("/git/refs/heads/" + BRANCH), {"sha": commit})
    print("pushed %s -> %s (%d files)" % (BRANCH, commit[:10], len(entries)))
    return commit


def main(argv):
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(__doc__)
        return 0
    if argv[0] == "head":
        print(head_sha())
        return 0
    if argv[0] != "push":
        raise SystemExit(__doc__)
    message = argv[1] if len(argv) > 1 else "update"
    rest = argv[2:]
    deletes, paths, use_git = [], [], False
    i = 0
    while i < len(rest):
        if rest[i] == "--delete":
            i += 1
            deletes.append(rest[i])
        elif rest[i] == "--all-changed":
            use_git = True
        else:
            paths.append(rest[i])
        i += 1
    root = os.getcwd()
    if use_git:
        paths = sorted(set(paths) | set(changed_files(root)))
    push(paths, message, deletes, root)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
