#!/usr/bin/env python3
"""Find and purge secrets from git HISTORY of a blobless (partial) clone, without downloading GBs.

  python3 tools/rsi/history_scrub.py scan  [ref ...]    # list leaking blobs (masked), refs default: origin/main
  python3 tools/rsi/history_scrub.py scrub [ref ...]    # rewrite history objects offline, print old->new tips
  python3 tools/rsi/history_scrub.py push  main=<new>   # tiny pack + receive-pack POST (see warning)

WHY NOT filter-repo / git push: both lazy-fetch every missing blob of a partial clone (multi-GB, the push
of a rewritten history grew .git from 0.6 to 4.5 GB and then disconnected). This tool only reads text blobs,
rewrites trees along the affected directories and sends ~1 MB. Tips with identical trees keep file contents
byte for byte; GPG signatures of rewritten commits are dropped (they could not verify anyway).
Secrets are never printed: matches are shown as sha256 prefixes. PAT comes from /tmp/gitenv.sh (GIT_ASKPASS).
"""
from __future__ import annotations
import base64, collections, hashlib, os, re, subprocess, sys, threading, urllib.request

os.environ["GIT_NO_LAZY_FETCH"] = "1"
VENDOR = re.compile(r"(\.bundle\.js|\.min\.js|/vendor/|excalidraw)", re.I)  # public sample keys, not ours
BINARY = re.compile(r"\.(svg|pdf|webp|jpe?g|png|gif|ico|docx?|woff2?|ttf|otf|ogg|mp[34]|whl|wasm|pyc|so|zip|gz|bin|onnx|apk|aab|jar|exe)$", re.I)
PATTERNS = [  # (regex, replacement)
    (rb"gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{40,}", b"[REDACTED_GITHUB_TOKEN]"),
    (rb"AKIA[0-9A-Z]{16}", b"[REDACTED_AWS_KEY]"),
    (rb"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]{20,3000}?-----END [A-Z ]*PRIVATE KEY-----", b"[REDACTED_PRIVATE_KEY]"),
    (rb"redis://[^\s:@/]*:[^\s@/]{6,}@[^\s'\"]+", b"redis://[REDACTED]"),
    (rb"nebians-admin-2024-secure-token", b"REDACTED-LEGACY-ADMIN-TOKEN"),
]
RX = [(re.compile(p), r) for p, r in PATTERNS]


def git(*a, inp=None, lazy=False):
    env = dict(os.environ)
    if lazy:
        env.pop("GIT_NO_LAZY_FETCH", None)
    return subprocess.run(["git", *a], input=inp, capture_output=True, check=True, env=env).stdout


def history_blobs(refs):
    """oid -> {paths}, from tree diffs only (needs no blobs). Gitlinks skipped."""
    out = collections.defaultdict(set)
    raw = git("log", *refs, "--raw", "--no-abbrev", "--no-renames", "--format=").decode(errors="replace")
    for ln in raw.splitlines():
        m = re.match(r":(\d+) (\d+) (\w+) (\w+) (\w)\t(.*)", ln)
        if m and m[2] != "160000" and m[1] != "160000" and set(m[4]) != {"0"}:
            out[m[4]].add(m[6])
    return out


def load(oids):
    """Yield (oid, bytes) for local blobs; fetch missing ones from the promisor remote first."""
    def check(ids):
        p = subprocess.run(["git", "cat-file", "--batch-check"], input=("\n".join(ids) + "\n").encode(), capture_output=True)
        return [o for o, ln in zip(ids, p.stdout.decode().splitlines()) if not ln.endswith("missing")]

    present = set(check(oids))
    missing = [o for o in oids if o not in present]
    if missing:
        env = {k: v for k, v in os.environ.items() if k != "GIT_NO_LAZY_FETCH"}
        env["GIT_TERMINAL_PROMPT"] = "0"
        env.setdefault("GIT_ASKPASS", "/tmp/gitenv.sh")
        for i in range(0, len(missing), 4000):
            subprocess.run(["git", "-c", "fetch.negotiationAlgorithm=noop", "fetch", "origin", "--no-tags", "--no-write-fetch-head",
                            "--recurse-submodules=no", "--filter=blob:none", "--stdin"],
                           input=("\n".join(missing[i:i + 4000]) + "\n").encode(), env=env, capture_output=True)
        present = set(check(oids))
    oids = [o for o in oids if o in present]
    print(f"scanning {len(oids)} text blobs", file=sys.stderr)
    p = subprocess.Popen(["git", "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    threading.Thread(target=lambda: (p.stdin.write(("\n".join(oids) + "\n").encode()), p.stdin.close()), daemon=True).start()
    for o in oids:
        h = p.stdout.readline().split()
        if len(h) < 3 or h[1] != b"blob":
            continue
        n = int(h[2])
        yield o, p.stdout.read(n + 1)[:n]


def find(refs):
    bp = history_blobs(refs)
    oids = sorted(o for o, ps in bp.items() if any(not BINARY.search(x) and not VENDOR.search(x) for x in ps))
    hits = {}
    for o, d in load(oids):
        nd = d
        for r, s in RX:
            nd = r.sub(s, nd)
        if nd != d:
            hits[o] = nd
    return bp, hits


def cmd_scan(refs):
    bp, hits = find(refs)
    print(f"{len(bp)} blobs in history, {len(hits)} leaking")
    for o in sorted(hits)[:40]:
        d = git("cat-file", "blob", o)
        kinds = [hashlib.sha256(m.group(0)).hexdigest()[:8] for r, _ in RX for m in r.finditer(d)][:3]
        print(" ", o[:10], sorted(bp[o])[0][:70], kinds)
    return 1 if hits else 0


def cmd_scrub(refs):
    bp, bmap_data = find(refs)
    bmap = {o: git("hash-object", "-w", "--stdin", inp=d).decode().strip() for o, d in bmap_data.items()}
    dirs = {"/".join(p.split("/")[:i]) for o in bmap for p in bp[o] for i in range(len(p.split("/")))}
    tc, memo, cmap = {}, {}, {}

    def ents(t):
        if t not in tc:
            tc[t] = [(m, ty, oid.decode(), n) for e in git("ls-tree", "-z", t).split(b"\0") if e
                     for (m, ty, oid), n in [(e.split(b"\t", 1)[0].split(), e.split(b"\t", 1)[1])]]
        return tc[t]

    def rt(t, pre):
        if (t, pre) in memo:
            return memo[t, pre]
        new, ch = [], False
        for m, ty, oid, n in ents(t):
            path = (pre + "/" if pre else "") + n.decode(errors="surrogateescape")
            if ty == b"blob" and oid in bmap:
                oid, ch = bmap[oid], True
            elif ty == b"tree" and path in dirs:
                x = rt(oid, path)
                ch, oid = ch or x != oid, x
            new.append((m, ty, oid, n))
        memo[t, pre] = t if not ch else git("mktree", "-z", inp=b"".join(m + b" " + ty + b" " + o.encode() + b"\t" + n + b"\0" for m, ty, o, n in new)).decode().strip()
        return memo[t, pre]

    for c in git("rev-list", "--topo-order", "--reverse", *refs).decode().split():
        head, _, msg = git("cat-file", "commit", c).partition(b"\n\n")
        out, skip, ch = [], False, False
        for ln in head.split(b"\n"):
            if skip and ln.startswith(b" "):
                continue
            skip = False
            if ln.startswith(b"tree "):
                nt = rt(ln[5:].decode(), ""); ch |= nt != ln[5:].decode(); out.append(b"tree " + nt.encode())
            elif ln.startswith(b"parent "):
                np_ = cmap[ln[7:].decode()]; ch |= np_ != ln[7:].decode(); out.append(b"parent " + np_.encode())
            elif ln.startswith(b"gpgsig"):
                skip = ch = True
            else:
                out.append(ln)
        cmap[c] = c if not ch else git("hash-object", "-t", "commit", "-w", "--stdin", inp=b"\n".join(out) + b"\n\n" + msg).decode().strip()
    for r in refs:
        o = git("rev-parse", r).decode().strip()
        print(f"{r} {o} -> {cmap[o]}  tree-equal={git('rev-parse', o + '^{tree}') == git('rev-parse', cmap[o] + '^{tree}')}")
    print(f"{len(bmap)} blobs redacted, {sum(a != b for a, b in cmap.items())} commits rewritten")


def cmd_push(args):
    """args: remote_ref=<new sha> ... ; old values are read from `git ls-remote` (a lease: stale = server rejects)."""
    pat = open("/tmp/gitenv.sh").read().split()[-1]
    auth = "Basic " + base64.b64encode(f"NikitHamal:{pat}".encode()).decode()
    base = "https://github.com/NikitHamal/NEB.git"
    ls = dict(reversed(l.split("\t")) for l in subprocess.run(["git", "ls-remote", "origin"], capture_output=True, text=True,
              env={**os.environ, "GIT_ASKPASS": "/tmp/gitenv.sh", "GIT_TERMINAL_PROMPT": "0"}).stdout.splitlines())
    ups = [("refs/heads/" + a.split("=")[0], ls["refs/heads/" + a.split("=")[0]], a.split("=")[1]) for a in args]
    rev = [f"{n}\n" for _, _, n in ups] + [f"^{o}\n" for _, o, _ in ups]
    rev += [f"^{t}\n" for t in sorted(set(git("log", *[o for _, o, _ in ups], "--format=%T").decode().split()))]
    pack = subprocess.run(["git", "pack-objects", "--revs", "--stdout", "--delta-base-offset"], input="".join(rev).encode(), capture_output=True).stdout
    pkt = lambda b: b"%04x" % (len(b) + 4) + b
    body = b"".join(pkt(f"{o} {n} {r}".encode() + (b"\0 report-status agent=rsi" if i == 0 else b"")) for i, (r, o, n) in enumerate(ups)) + b"0000" + pack
    rq = urllib.request.Request(base + "/git-receive-pack", data=body, headers={"Authorization": auth, "Content-Type": "application/x-git-receive-pack-request"})
    print(urllib.request.urlopen(rq, timeout=170).read().decode(errors="replace").replace(pat, "***")[-300:])


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("scan", "scrub", "push"):
        sys.exit(__doc__)
    a = sys.argv[2:]
    if sys.argv[1] == "push":
        cmd_push(a)
    else:
        sys.exit(globals()["cmd_" + sys.argv[1]](a or ["origin/main"]))
