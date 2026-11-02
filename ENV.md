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
