#!/usr/bin/env python3
"""Upload the NEBians book PDFs to the live library, one resource per book, from one account.

Standard library only (Python 3.8+). Listing data comes from manifest.json (see build_manifest.py);
nothing is typed here.

Credentials (environment, never in the repo):
    NEB_EMAIL, NEB_PASSWORD     sign in with the account that should own the books, or
    NEB_TOKEN                   an authToken from a previous sign in
    NEB_BASE_URL                default https://nebians.consica.com.np

Usage (run from the repo root):
    python tools/publish/publish_books.py --dry-run            # print what would be sent, touch nothing
    python tools/publish/publish_books.py                      # upload every book not yet published
    python tools/publish/publish_books.py --only phy11 cee-phy # some books
    python tools/publish/publish_books.py --level 12           # one level: Class 8, "Class 10 / SEE", 11, 12, "Entrance Prep", Bachelors

An upload lands as `pending` until it is approved. The admin API needs a staff session, so approve on the
server:  python manage.py approve_book_uploads <username> --yes   (lists first without --yes).
`published.json` (next to this file) records slug -> resource id, so a
second run skips finished books and a failed run resumes where it stopped. A book is also skipped when the
library already holds a resource with the same title from this account.
"""
import argparse
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
STATE = os.path.join(HERE, "published.json")
FIELDS = ("title", "description", "subject", "grade_level", "program", "faculty", "exam_type", "year",
          "tags", "type", "author_name", "source_label")


def call(base, method, path, token=None, body=None, content_type="application/json", retries=4):
    data = body if isinstance(body, (bytes, type(None))) else json.dumps(body).encode()
    for attempt in range(retries):
        req = urllib.request.Request(base + path, data=data, method=method)
        req.add_header("Accept", "application/json")
        req.add_header("User-Agent", "nebians-publisher/1.0")
        if data is not None:
            req.add_header("Content-Type", content_type)
        if token:
            req.add_header("Authorization", "Bearer " + token)
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                return r.status, json.loads(r.read() or b"{}")
        except urllib.error.HTTPError as e:
            raw = e.read()
            try:
                payload = json.loads(raw)
            except ValueError:
                payload = {"error": raw[:200].decode("utf8", "replace")}
            if e.code == 429 and attempt < retries - 1:
                wait = int(e.headers.get("Retry-After") or 30)
                print(f"  rate limited, waiting {wait}s")
                time.sleep(wait)
                continue
            return e.code, payload
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt == retries - 1:
                return 0, {"error": str(e)}
            time.sleep(5 * (attempt + 1))
    return 0, {"error": "gave up"}


def multipart(fields, files):
    boundary = uuid.uuid4().hex
    out = []
    for k, v in fields.items():
        out.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    for k, path in files.items():
        name = os.path.basename(path)
        mime = mimetypes.guess_type(name)[0] or "application/octet-stream"
        head = f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"; filename="{name}"\r\nContent-Type: {mime}\r\n\r\n'
        with open(path, "rb") as f:
            out += [head.encode(), f.read(), b"\r\n"]
    out.append(f"--{boundary}--\r\n".encode())
    return b"".join(out), f"multipart/form-data; boundary={boundary}"


def sign_in(base):
    token = os.environ.get("NEB_TOKEN", "").strip()
    if token:
        return token
    email, password = os.environ.get("NEB_EMAIL", ""), os.environ.get("NEB_PASSWORD", "")
    if not (email and password):
        sys.exit("Set NEB_TOKEN, or NEB_EMAIL and NEB_PASSWORD.")
    status, res = call(base, "POST", "/api/auth/email/login/", body={"email": email, "password": password})
    if status != 200 or not res.get("authToken"):
        sys.exit(f"Sign in failed ({status}): {res.get('error', res)}")
    print("Signed in as", res.get("user", {}).get("username") or email)
    return res["authToken"]


def already_listed(base, token, title):
    q = urllib.parse.urlencode({"search": title})
    status, res = call(base, "GET", "/api/resources/?" + q, token=token)
    items = res if isinstance(res, list) else res.get("resources") or res.get("results") or []
    return next((r.get("id") for r in items if (r.get("title") or "").strip() == title), None)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--only", nargs="*", default=[], help="slugs to upload")
    ap.add_argument("--level", help="only this grade_level value")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-cover", action="store_true", help="do not send the cover image")
    ap.add_argument("--pause", type=float, default=2.0, help="seconds between uploads")
    args = ap.parse_args()

    manifest = json.load(open(os.path.join(HERE, "manifest.json"), encoding="utf-8"))
    base = (os.environ.get("NEB_BASE_URL") or manifest["site"]).rstrip("/")
    books = [b for b in manifest["books"]
             if (not args.only or b["slug"] in args.only) and (not args.level or b["grade_level"] == args.level)]
    if args.only:
        unknown = set(args.only) - {b["slug"] for b in manifest["books"]}
        if unknown:
            sys.exit("Unknown slug: " + ", ".join(sorted(unknown)))
    state = json.load(open(STATE)) if os.path.exists(STATE) else {}

    token = None if args.dry_run else sign_in(base)
    done = failed = skipped = 0
    for i, b in enumerate(books, 1):
        pdf = os.path.join(REPO, b["file"])
        tag = f"[{i}/{len(books)}] {b['slug']}"
        if b["slug"] in state:
            print(tag, "already published", state[b["slug"]])
            skipped += 1
            continue
        if not os.path.exists(pdf):
            print(tag, "PDF missing:", b["file"])
            failed += 1
            continue
        if args.dry_run:
            print(tag, "|", b["title"], "|", b["grade_level"], "|", b["program"] or "-", "|",
                  f"{os.path.getsize(pdf) / 1048576:.1f} MB")
            print("    ", b["description"])
            continue
        existing = already_listed(base, token, b["title"])
        if existing:
            print(tag, "title already in the library", existing)
            state[b["slug"]] = existing
            skipped += 1
            continue
        fields = {k: b.get(k, "") for k in FIELDS}
        if b.get("is_paid"):
            fields["is_paid"] = "true"
        files = {"file": pdf}
        cover = os.path.join(HERE, b.get("cover", ""))
        if not args.no_cover and b.get("cover") and os.path.exists(cover):
            files["thumbnail"] = cover
        body, ctype = multipart(fields, files)
        print(tag, "uploading", f"{len(body) / 1048576:.1f} MB")
        status, res = call(base, "POST", "/api/resources/upload/", token=token, body=body, content_type=ctype)
        if status not in (200, 201):
            print("   FAILED", status, res.get("error", res))
            failed += 1
            continue
        rid = res.get("id")
        state[b["slug"]] = rid
        json.dump(state, open(STATE, "w"), indent=1)
        print("   created", rid, "(pending: approve with manage.py approve_book_uploads)")
        done += 1
        time.sleep(args.pause)
    if not args.dry_run:
        json.dump(state, open(STATE, "w"), indent=1)
    print(f"\n{done} uploaded, {skipped} skipped, {failed} failed, {len(books)} selected")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
