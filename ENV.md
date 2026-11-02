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
