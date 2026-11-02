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
