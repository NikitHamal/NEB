# POLISH_ENV.md — school-books polish session probe

Branch: polish/school-books-claude (from main f372ce8). Real output, captured this session. PAT is passed per-command via an http.extraheader and is not in any file or git config.

## git
```
git version 2.39.5
/usr/bin/git
```
## ls-remote (private repo: anonymous fails, authenticated works)
```
$ git ls-remote https://github.com/NikitHamal/NEB.git   # anonymous
fatal: could not read Username for 'https://github.com': No such device or address
$ (authenticated, first 6 refs)
f372ce84c3af8993b54bf6f3f6054c45ea57dcf9	refs/heads/main
f372ce84c3af8993b54bf6f3f6054c45ea57dcf9	refs/heads/polish/school-books-claude
```
## origin/main log (20)
```
f372ce8 desktop: History, Help, Privacy/Terms screens; menu bar; offline banner; Ctrl+D downloads; chip/stat spacing; home tile copy
41918dc backend: avatar/profile endpoint tests (23 passing with content + desktop auth)
ed34f1c backend: README (env vars, DB, docker, deploy), Dockerfile, docker-compose, .env.example
dac1a7b docs: ENV.md session probe, desktop/STATUS.md audit of remote state
481bbc4 ci(desktop): workflow builds and attaches only the Windows .exe + sha256; desktop: avatars on sidebar, profile, community, stale-while-offline image cache
d61169a desktop: server-backed content with disk cache (no content folder), books, offline manager, people & member profiles, avatars, new auth layout; menu bar removed
4475fcd backend: read-only content API for the desktop app (manifest, syllabus, chapters, search, books with Range), 8 tests
2193bf3 auth, web: fix desktop auth csrf and logo, polish resource comments ui
3b470dd web: reduce left and right side margins across all page containers
e3e29c1 Merge branch 'desktop/claude' into main
2beba85 web: harmonize page layouts and eliminate desktop scrim overlay
bac4504 desktop: v0.2.0 — Windows .exe, 31 screenshots, docs (backend, parity, design, architecture, build, limitations)
44eaba0 desktop: Material 3 Expressive redesign — Material Icons font, M3 palette/widgets, nav rail, Google/GitHub/email sign-in via browser hand-off, community, notifications, profile sync, live e2e handoff test
6fff2ad backend: desktop browser hand-off sign-in (PKCE start/poll + consent page), 10 tests
4252b62 desktop: BUILD.md with real errors/fixes and fresh-clone build result
c7121ff desktop: docs (parity, design, architecture, limitations), scripts, CI workflow, Windows x86_64 .exe
046ce20 desktop: reader jump settles after late figure loads; screenshots (22) from the real app; cargo config for mingw
a01112d desktop: native Rust/egui app — theme, data layer, reader engine, all screens, shell
15df55b desktop: ENV.md — real environment probes (git, network, rust, mingw target)
bb19a74 api: LongCat 2.0 -> 2.5, and the thinking / web-search flags actually wired
```
## toolchain
```
Python 3.11.2
weasyprint 70.0
pandoc: /usr/bin/pandoc
pdftoppm: /usr/bin/pdftoppm
pdftotext: /usr/bin/pdftotext
/bin/bash: line 11: rustc: command not found
v22.23.4
HTTP/2 200 
```
## install notes (honest)
- weasyprint was initially absent: `ModuleNotFoundError`. Installed with `pip install --break-system-packages weasyprint markdown matplotlib numpy pymupdf pyyaml pillow` (PEP 668 blocks plain pip), then `sudo apt-get update && apt-get install libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0 poppler-utils pandoc` (first import failed on libpango).
- rustc is not installed; it is not needed for the school-book pipeline (desktop app only), so it was not installed.

## Session 3 (continuation) — env + baseline verify
Sandbox was a bare Vite project; repo re-cloned (shallow, branch only), PAT supplied via GIT_ASKPASS env var, not in .git/config or any file.
```
$ git --version && which git
git version 2.39.5
/usr/bin/git
$ git ls-remote origin polish/school-books-claude  (authenticated)
5a441618c9b24a27d49ac9b1d0fc036a091ac02e	refs/heads/polish/school-books-claude
$ system python3 (3.11, NOT used for the pipeline)
Python 3.11.2
$ build venv: uv venv --python 3.12
Python 3.12.16
weasyprint 70.0
$ which pandoc pdftoppm pdftotext; node --version
/usr/bin/pandoc
/usr/bin/pdftoppm
/usr/bin/pdftotext
v20.20.2
$ curl -sI https://github.com | head -1
HTTP/2 200 
$ fc-list : family (book fonts)
Inter
JetBrains Mono
Noto Sans Devanagari
Poppins
Poppins Light
Poppins SemiBold
Source Serif 4
```
Fonts: not vendored. Located via `notes/pipeline/fonts/install.sh` (downloads from github.com/google/fonts into ~/.local/share/fonts/nebians). All five families (Poppins, Inter, Source Serif 4, Noto Sans Devanagari, JetBrains Mono) installed and visible to fontconfig before any build; no wrong-font builds.
Python 3.12 obtained with `pip install uv; uv python install 3.12` (Debian 12 only ships 3.11).
