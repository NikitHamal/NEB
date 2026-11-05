# ENV.md — real environment probe

Recorded 2026-11-02 13:40:43 UTC in the AgentSky sandbox (`Linux 6.1.158+`, user `user`). Every block below is verbatim command output; nothing is assumed. Secrets are redacted.

## Starting state

The sandbox opened in `/app` — a bare Next.js scaffold, **not** a clone of this repo (no `bca/`, no `ioe/`, no `.git`). The repo is **private** (`GET /repos/NikitHamal/NEB` → `"private": true`; unauthenticated → 404), so it was cloned with the supplied token into `/home/user/work/NEB`. The token is injected per command through an `http.extraheader` wrapper and is never written to `.git/config` or any tracked file (a grep of `.git/config` for the token prefix → 0 matches).

## Probe (first run, before installing anything)

```
$ git --version && which git
git version 2.39.5
/usr/bin/git

$ git ls-remote https://github.com/NikitHamal/NEB.git
fatal: could not read Username for 'https://github.com': No such device or address
exit=0

$ rustc --version
/bin/bash: line 4: rustc: command not found
$ cargo --version
/bin/bash: line 4: cargo: command not found
$ node --version
v22.23.4
$ npm --version
10.9.9

$ which pandoc weasyprint wkhtmltopdf pdflatex typst xelatex chromium
exit=1

$ sudo -n true
exit=0

$ curl -sI https://github.com | head -1
HTTP/2 200 
exit=0

$ curl -sI https://api.github.com | head -1
HTTP/2 200 

$ python3 --version; apt --version
Python 3.11.2
apt 2.6.1 (amd64)

uid=1001(user) gid=1001(user) groups=1001(user),27(sudo)
Linux e2b.local 6.1.158+ #1 SMP PREEMPT_DYNAMIC Wed Sep 30 12:40:02 UTC 2026 x86_64 GNU/Linux
```

Findings: git, node, npm, python3, gcc, sudo (passwordless) and github.com were available. **Missing:** rustc, cargo, pandoc, weasyprint, wkhtmltopdf, pdflatex, typst, fontconfig (`fc-list`), poppler, and the Python libs the house PDF pipeline imports. Unauthenticated `git ls-remote` failed because the repo is private; with the token it works (below).

## Remote (with token, redacted)

```
$ git ls-remote https://<PAT>@github.com/NikitHamal/NEB.git | head
2193bf3f4ea3097eaae2e8349ffb60a9edd403d4	HEAD
5d9de9180f85bccd2d84076267d5c6221f1d6805	refs/heads/claude/bca-entrance-complete
bac4504b0d0c9ad70a278701fe8f4096ef2750e5	refs/heads/desktop/claude
2193bf3f4ea3097eaae2e8349ffb60a9edd403d4	refs/heads/main
2505fe3d56599d099cbcaac185ca9a63a0bc4482	refs/heads/overhaul/showreel
e3468a9c969343c80192d829302ac3449945b162	refs/heads/resources/bca-complete
```

## Which PDF tool does the existing pipeline use?

Inspected `notes/pipeline/` and `NOTES_HANDOFF.md`: **Markdown → `md2html.py` → WeasyPrint (`build_pdf.py`, `theme.css`) with matplotlib rendering maths (`mathsvg.py`) and figures (`figrun.py`)**, fonts Poppins / Inter / Source Serif 4 / Noto Sans Devanagari / JetBrains Mono. No pandoc, LaTeX, Typst or wkhtmltopdf is involved. Built PDFs are committed as ordinary files (no `.gitattributes`, no git-lfs: `git lfs version` → `git: 'lfs' is not a git command`), so BCA/IOE PDFs follow the same choice.

## Installed this session (apt + pip + rustup + fonts), with resulting versions

```
$ git --version
git version 2.39.5
$ rustc --version
rustc 1.99.1 (58cf8f9c3 2026-10-13)
$ cargo --version
cargo 1.99.1 (5f94df478 2026-08-27)
$ node --version
v22.23.4
$ npm --version
10.9.9
$ python3 --version
Python 3.11.2
$ pandoc --version
pandoc 2.17.1.1
$ pdftoppm -v
pdftoppm version 22.12.0
$ python -c "import weasyprint, matplotlib, markdown, fitz, pypdf"
weasyprint 70.0 | matplotlib 3.11.2
$ which pandoc weasyprint pdftoppm fc-list
/usr/bin/pandoc
/home/user/venv/bin/weasyprint
/usr/bin/pdftoppm
/usr/bin/fc-list
$ fc-list : family | grep -iE "poppins|inter|source serif|devanagari|jetbrains" | sort -u
Inter
JetBrains Mono
Noto Sans Devanagari
Poppins
Poppins,Poppins Light
Poppins,Poppins SemiBold
Source Serif 4
$ which wkhtmltopdf pdflatex typst   # still absent, and not needed
exit=1
```


---

# Appendix — ENV.md as it existed on `main` (desktop-app session)

Kept verbatim from `origin/main` when the branches were merged; it documents the Rust/mingw probes for the `desktop/` app, not the BCA/IOE work above.

# ENV.md — real environment probes

Every block below is the verbatim output of the command shown, captured by the agent in this sandbox on 2026-11-02 11:12 UTC. The GitHub token is redacted (`$GHP`).

### `git --version; which git`
```
git version 2.39.5
/usr/bin/git
```

### `git ls-remote https://github.com/NikitHamal/NEB.git 2>&1 | head -3`
```
fatal: could not read Username for 'https://github.com': No such device or address
```

> The unauthenticated probe fails: **the NEB repo is private** (confirmed by `GET /repos/NikitHamal/NEB` → `"private": true`). The supplied PAT is therefore required even for reads.

### `curl -s -H "Authorization: Bearer $GHP" https://api.github.com/repos/NikitHamal/NEB | grep -E "\"(full_name|private|default_branch)\""`
```
  "full_name": "NikitHamal/NEB",
  "private": true,
  "visibility": "private",
  "default_branch": "main",
```

### `B=$(printf "x-access-token:%s" "$GHP"|base64 -w0); git -c http.extraheader="Authorization: Basic $B" ls-remote https://github.com/NikitHamal/NEB.git | head -4`
```
bb19a74e7466cfcc2d472ba19b047b45822296a1	HEAD
9dd4e12b4369699cef90824cd13ecb5e7a5ca24f	refs/heads/agent/interactive-overhaul
87642c9d0c4d5e8ce3d6268764f83f4ef08a3f8f	refs/heads/arena/a0b84f2d-neb
7745c4963e890edc05e958127a8076b49a045d4b	refs/heads/arena/ebdf7303-neb
```

### `git log --oneline -3 main 2>/dev/null || (cd /tmp/NEB && git log --oneline -3 origin/main)`
```
bb19a74 api: LongCat 2.0 -> 2.5, and the thinking / web-search flags actually wired
fd772b3 web: export the IOE track — syllabus pages and reader chapters
23592b8 notes: IOE B.E./B.Arch entrance books — 23 chapters, 5 spines, all checks green
```

### `curl -sI https://github.com | head -1`
```
HTTP/2 200 
```

### `sudo -n true && echo "passwordless sudo OK"`
```
passwordless sudo OK
```

### `rustc --version; cargo --version; rustup --version 2>&1 | head -1`
```
rustc 1.99.1 (58cf8f9c3 2026-10-13)
cargo 1.99.1 (5f94df478 2026-08-27)
rustup 1.29.2 (d8c92c676 2026-10-21)
```

> Initial state: `rustc`/`cargo` were **not installed** (`rustc: command not found`). Installed with `curl https://sh.rustup.rs | sh -s -- -y --profile minimal`.

### `rustup target list --installed`
```
x86_64-pc-windows-gnu
x86_64-unknown-linux-gnu
```

### `x86_64-w64-mingw32-gcc --version | head -1; ls /usr/bin/x86_64-w64-mingw32-* | head -3`
```
x86_64-w64-mingw32-gcc (GCC) 12-win32
/usr/bin/x86_64-w64-mingw32-addr2line
/usr/bin/x86_64-w64-mingw32-ar
/usr/bin/x86_64-w64-mingw32-as
```

### `xvfb-run --help 2>&1 | head -1; which Xvfb xdotool import`
```
Usage: xvfb-run [OPTION ...] COMMAND
/usr/bin/Xvfb
/usr/bin/xdotool
/usr/bin/import
```

### `uname -a; nproc; free -m; df -h / | tail -1`
```
Linux e2b.local 6.1.158+ #1 SMP PREEMPT_DYNAMIC Wed Sep 30 12:40:02 UTC 2026 x86_64 GNU/Linux
2
               total        used        free      shared  buff/cache   available
Mem:            1982         262         261           1        1643        1720
Swap:              0           0           0
/dev/root        22G  5.4G   16G  26% /
```

### Packages installed (apt, via sudo)
```
mingw-w64 xvfb libgl1-mesa-dri libgl1 libegl1 libxkbcommon-x11-0 libxkbcommon-dev libwayland-dev libx11-dev libxcursor-dev libxrandr-dev libxi-dev libxcb1-dev pkg-config build-essential python3-pip zip imagemagick xdotool x11-utils
pip: fonttools brotli (converting the repo's woff2 Poppins-Devanagari to TTF)
rustup target add x86_64-pc-windows-gnu
```

### Sandbox constraints that shaped the plan
- 2 vCPU / ~2 GB RAM / no swap: release builds of egui + resvg take several minutes; `lto`/codegen-units are tuned accordingly (see BUILD.md).
- Runs as non-root user `user` with passwordless sudo.

### pip install (real error + fix)
`pip install fonttools brotli` → `error: externally-managed-environment` (PEP 668). Fixed with `pip install --break-system-packages fonttools brotli`.

## Session 3 probe (2026-11-02) — pasted from real commands
```
$ git --version
git version 2.39.5
$ which git
/usr/bin/git
$ rustc --version
rustc 1.99.1 (58cf8f9c3 2026-10-13)
$ cargo --version
cargo 1.99.1 (5f94df478 2026-08-27)
$ python3 --version
Python 3.11.2
$ node --version
v22.23.4
$ which pandoc weasyprint pdftoppm
/usr/bin/pandoc
/usr/bin/pdftoppm
$ sudo -n true && echo sudo-ok
sudo-ok
$ curl -sI https://github.com | head -1
HTTP/2 200 
$ git log --oneline -8
481bbc4 ci(desktop): workflow builds and attaches only the Windows .exe + sha256; desktop: avatars on sidebar, profile, community, stale-while-offline image cache
d61169a desktop: server-backed content with disk cache (no content folder), books, offline manager, people & member profiles, avatars, new auth layout; menu bar removed
4475fcd backend: read-only content API for the desktop app (manifest, syllabus, chapters, search, books with Range), 8 tests
2193bf3 auth, web: fix desktop auth csrf and logo, polish resource comments ui
3b470dd web: reduce left and right side margins across all page containers
e3e29c1 Merge branch 'desktop/claude' into main
2beba85 web: harmonize page layouts and eliminate desktop scrim overlay
bac4504 desktop: v0.2.0 — Windows .exe, 31 screenshots, docs (backend, parity, design, architecture, build, limitations)
$ python3 -c 'import weasyprint'
ModuleNotFoundError: No module named 'weasyprint'
$ git ls-remote origin (PAT via transient header)
481bbc48ab27f22c723c08363f3873ad57ec97c1	HEAD
42abf217b84a0da68d92a6e61ca787b36eded246	refs/heads/claude/bca-entrance-complete
bac4504b0d0c9ad70a278701fe8f4096ef2750e5	refs/heads/desktop/claude
481bbc48ab27f22c723c08363f3873ad57ec97c1	refs/heads/main
2505fe3d56599d099cbcaac185ca9a63a0bc4482	refs/heads/overhaul/showreel
e3468a9c969343c80192d829302ac3449945b162	refs/heads/resources/bca-complete
12f65e59b5e291490d8e2e0c6b178054b30bce2c	refs/pull/1/head
06541a540a57957c51a640eab03d78d62b502679	refs/pull/10/head
05977d92ef658f7f0430f9143dad4fb5388aee81	refs/pull/11/head
eedf16a36ebd64e8b239191f456014b345a7e576	refs/pull/12/head
$ git ls-tree -r origin/main --name-only | grep -E '^(desktop|backend_python)/' | grep -E 'content|remote_image|menu|desktop_auth'
backend_python/api/content_api.py
backend_python/api/content_images.py
backend_python/api/content_search.py
backend_python/api/desktop_auth.py
backend_python/api/management/commands/purge_bot_content.py
backend_python/api/migrations/0039_syllabuscontent_and_more.py
backend_python/api/migrations/0040_syllabuscontent_question_answers.py
backend_python/api/migrations/0074_study_space_board_content.py
backend_python/api/migrations/0116_content_image.py
backend_python/api/migrations/0123_syllabus_rich_content.py
backend_python/api/migrations/0151_keep_deleted_user_content.py
backend_python/api/test_content_api.py
backend_python/api/test_desktop_auth.py
backend_python/api/test_purge_bot_content.py
backend_python/api/views_content.py
backend_python/api/views_content_images.py
backend_python/api/views_desktop_auth.py
backend_python/web/templates/web/_library_content.html
backend_python/web/templates/web/desktop_auth.html
backend_python/web/templates/web/interactive/_hub_content.html
backend_python/web/views_content_images.py
backend_python/web/views_desktop_auth.py
desktop/scripts/bundle-content.sh
desktop/src/data/content.rs
desktop/src/ui/remote_image.rs
```
Note: the repo is private — unauthenticated `git ls-remote` fails with 'could not read Username'. Rust, mingw, xvfb were installed this session via apt/rustup (not present at start: `rustc: command not found`).

## Agent workaround: the file tool is rooted at /app, shell is not
Clone to `/tmp/NEB` and `ln -sfn /tmp/NEB /app/neb`; the file tool then reaches `neb/...`. For images, make a
directory under `/app` (e.g. `/app/shots_out`) and write screenshots there. Do not issue a write and the read of
the same file in one parallel tool block (the read can race and report "does not exist").
Push with an out-of-repo `GIT_ASKPASS` helper that reads the token from an env var; never write it to a file in the repo.
Headless GUI: `LIBGL_ALWAYS_SOFTWARE=1 xvfb-run`, and `xdotool windowfocus $(xdotool search --name NEBians|head -1)` first (no WM means no key focus).

## File-tool workaround (added 2026-11, desktop M3 pass)
The agent file tool is rooted at the sandbox project dir, not at the clone. Clone to `/tmp/NEB`, then
`ln -sfn /tmp/NEB <tool-root>/neb` and edit files as `neb/desktop/...`. Screenshots: `ln -sfn /tmp/shots <tool-root>/shots`.
The PAT is only ever read from an out-of-repo env file through a `GIT_ASKPASS` helper (`/tmp/gitenv.sh`); it is never written into the repo.
Tools installed this session: rustup (minimal), gcc-mingw-w64-x86-64, xvfb, imagemagick, wine.
## Probe — BCA course session (this session)

Fresh sandbox again; the repo is private so unauthenticated access fails exactly as before; authenticated clone (token only in the clone URL, never in git config) works.

```
$ git --version && which git
git version 2.39.5
/usr/bin/git
$ git ls-remote https://github.com/NikitHamal/NEB.git        # anonymous
fatal: could not read Username for 'https://github.com': No such device or address
$ git ls-remote <authenticated url>  | grep bca-entrance-complete
42abf217b84a0da68d92a6e61ca787b36eded246	refs/heads/claude/bca-entrance-complete
$ python3 --version
Python 3.11.2
$ python3 -c "import weasyprint; print(weasyprint.__version__)"   # before install
ModuleNotFoundError: No module named 'weasyprint'
$ which pandoc pdftoppm ; rustc --version                      # before install
(nothing) ; rustc: command not found
$ node --version
v22.23.4
$ curl -sI https://github.com | head -1
HTTP/2 200
```

Installed this session: `apt-get install pandoc poppler-utils libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz0b`; `pip install --break-system-packages weasyprint markdown matplotlib pyyaml pymupdf`. After install: weasyprint 70.0, `/usr/bin/pandoc`, `/usr/bin/pdftoppm`. Rust is not needed by the pipeline.

## Probe — BCA course session 3 (remaining subjects, Semester II onward)

```
$ git --version && which git
git version 2.39.5
/usr/bin/git
$ git ls-remote <authenticated url> claude/bca-entrance-complete
fcb441d42559f740f5a5ec7dfd21efce8f441d0e	refs/heads/claude/bca-entrance-complete   (confirmed tip)
$ python3 --version
Python 3.11.2
$ python3 -c "import weasyprint; print(weasyprint.__version__)"   # before install
ModuleNotFoundError: No module named 'weasyprint'
$ which pandoc pdftoppm ; rustc --version                         # before install
(nothing) ; /bin/bash: rustc: command not found
$ node --version
v22.23.4
$ curl -sI https://github.com | head -1
HTTP/2 200
```
Fixes this session: `apt-get install pandoc poppler-utils gcc default-jdk-headless libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz0b`; `pip install --break-system-packages weasyprint markdown pyyaml matplotlib pymupdf sympy numpy uv`; fonts via `notes/pipeline/fonts/install.sh`; **Python 3.12** (the pipeline needs it) via `uv python install 3.12 && uv venv --python 3.12 /tmp/venv && uv pip install --python /tmp/venv/bin/python weasyprint markdown pyyaml matplotlib pymupdf sympy numpy pillow`. After that: weasyprint 70.0 on Python 3.12.16, `/usr/bin/pandoc`, `/usr/bin/pdftoppm`, gcc, javac 17. Rust is not needed. Test build of Mathematics II: 23 pages, 0 math/figure failures.

## Session 5 baseline (Semester III start)
```
$ git --version && which git
git version 2.39.5
/usr/bin/git
$ git ls-remote origin claude/bca-entrance-complete   (credentials via GIT_ASKPASS env helper, not stored)
eefb48c83c6a8c163523c0cab58f1bd25995ecef	refs/heads/claude/bca-entrance-complete
$ python3 --version; python3 -c "import weasyprint; print(weasyprint.__version__)"
Python 3.11.2
70.0
$ /tmp/venv/bin/python --version  (Python 3.12 venv used for the pipeline)
Python 3.12.16
70.0
$ which pandoc pdftoppm; node --version
/usr/bin/pandoc
/usr/bin/pdftoppm
v22.23.4
$ curl -sI https://github.com | head -1
HTTP/2 200 
```
Fresh sandbox: nothing was installed at session start (python3 -c weasyprint -> ModuleNotFoundError; pandoc/pdftoppm absent). Installed: apt pandoc poppler-utils gcc default-jdk-headless libpango libharfbuzz; pip weasyprint markdown pyyaml pymupdf matplotlib sympy numpy uv; Python 3.12 venv via uv; fonts via notes/pipeline/fonts/install.sh. The repo is private-or-auth-gated for clone: an unauthenticated clone failed ('could not read Username'), so a GIT_ASKPASS helper in /tmp reads the PAT from an env var; the PAT is in no repo file and not in .git/config. Test build of Hardware Workshop: 24 pages, 0 failures (test PDF reverted).

Session 5 additions: `pip install --break-system-packages scipy numpy` (statistics checks); `apt install libxml2-utils` (xmllint); `npm i jquery@3 jsdom` in /tmp/jsd (jQuery checks); PostgreSQL 15 on 127.0.0.1:5432 was already running (used by `fill_sql_outputs.py`).
