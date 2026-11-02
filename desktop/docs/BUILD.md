# Building

## Linux (native)
```bash
sudo apt install build-essential pkg-config libxkbcommon-dev libwayland-dev libx11-dev libxcursor-dev libxrandr-dev libxi-dev libgl1-mesa-dev
curl https://sh.rustup.rs | sh -s -- -y         # if Rust is missing
cd desktop && cargo build --release              # or: scripts/build.sh
./target/release/nebians --content ..            # content = the NEB checkout
```
Result: one ~13 MB stripped binary (`target/release/nebians`). Release profile: `opt-level=3`, thin LTO, `codegen-units=8`, `panic=abort`, `strip` — chosen so a build fits in 2 GB RAM / 2 cores.

## Windows `.exe`
### A. Cross-compile from Linux (done in this sandbox — a real `.exe` is committed)
```bash
sudo apt install mingw-w64
rustup target add x86_64-pc-windows-gnu
sudo update-alternatives --set x86_64-w64-mingw32-gcc /usr/bin/x86_64-w64-mingw32-gcc-posix   # std needs posix threads
cd desktop && cargo build --release --target x86_64-pc-windows-gnu      # or: scripts/build.sh windows
```
Produced: `target/x86_64-pc-windows-gnu/release/nebians.exe` (11 MB), copied to **`desktop/releases/nebians-windows-x86_64.exe`** with `SHA256SUMS`.
Verified with `x86_64-w64-mingw32-objdump -p`: PE32+ **GUI subsystem** (no console window), has a `.rsrc` section (icon + version info via `build.rs`/`winresource` + `assets/nebians.ico`), imports only system DLLs (`kernel32, user32, gdi32, opengl32, shell32, …`) — no MinGW runtime DLL is required next to it. `.cargo/config.toml` pins the linker.
**Not verified:** actually launching it — the sandbox has no Windows and I did not install wine. The Linux build of the same source was run and screenshotted.

### B. Native build on Windows
`scripts\build-windows.bat` or `scripts\build-windows.ps1` (needs Rust + the MSVC build tools), or let GitHub Actions do it: `.github/workflows/desktop-windows.yml` (`windows-latest`: tests, release build, bundles `nebians.exe` + `content/` as an artifact).

### Running it
The exe reads study content from disk. Either place it in a checkout of this repo (it walks up to find `backend_python/web/data`), run `nebians.exe --content C:\path\to\NEB`, or build a bundle:
```bash
scripts/bundle-content.sh windows          # dist/NEBians-Desktop-windows.zip  (exe + content/{data,static/web/study}); add --with-pdfs for the 42 book PDFs
```

## Screenshots
`scripts/screenshots.sh` runs the real binary under Xvfb with Mesa software GL and egui's own framebuffer capture (`--screenshots <dir>` drives a 22-step tour). The 22 PNGs in `desktop/screenshots/` came from exactly this.

## Real problems met while building, and the fixes
| Problem (verbatim symptom) | Fix |
|---|---|
| `rustc: command not found` | installed rustup (`rustc 1.99.1`) |
| `pip install` → `externally-managed-environment` (PEP 668) | `pip install --break-system-packages fonttools brotli` (used to convert the repo's woff2 Poppins-Devanagari to TTF) |
| `use of unresolved module or unlinked crate egui` | added `egui = "0.29"` as a direct dependency alongside `eframe` |
| `xvfb-run: error: xauth command not found` | `sudo apt install xauth` |
| `error[E0500]: closure requires unique access to *env` (settings groups) | helper fns take `&Theme` instead of `&Env` |
| Reader opened "Practice questions" short of the heading | late-loading SVGs shifted layout after the one-shot scroll; the jump is now re-applied for ~30 frames |
| `git ls-remote` asks for a username | repo is private — token passed as an `http.extraheader`, never stored in `.git/config` or any tracked file |

## Fresh-clone verification
`git clone --depth 1 --branch desktop/claude <repo> /tmp/fresh && cd /tmp/fresh/desktop && cargo build --release` on the pushed commit `c7121ff`, empty `target/`:
```
    Finished `release` profile [optimized] target(s) in 3m 00s
real	3m1.702s
user	5m24.719s
sys	0m26.223s
FRESH_EXIT 0
```
`./target/release/nebians --version` → `NEBians Desktop 0.1.0`.

---

# Session 2 build log (v0.2.0) — real results

**Linux:** `cd desktop && cargo build --release` → `Finished release profile [optimized]` (clean build ≈ 3.5 min on 2 vCPU; incremental ≈ 75 s).

**Windows `.exe`:** `rustup target add x86_64-pc-windows-gnu && cargo build --release --target x86_64-pc-windows-gnu` (linker `x86_64-w64-mingw32-gcc`, from `.cargo/config.toml`; needs `sudo apt install mingw-w64`) → `WIN_DONE`, `target/x86_64-pc-windows-gnu/release/nebians.exe`, 11.7 MB, a real PE32+ executable (`MZ` header, mingw `objdump` reports `pei-x86-64`). Copied to `releases/nebians-windows-x86_64.exe`; hash in `releases/SHA256SUMS`. It was **not launched** (no Windows/wine here); `.github/workflows/desktop-windows.yml` builds it natively on `windows-latest`.

**Screenshots:** 31 PNGs in `screenshots/`, produced by the running Linux build under Xvfb with software GL:
`xvfb-run -a -s "-screen 0 1400x900x24 +extension GLX" env LIBGL_ALWAYS_SOFTWARE=1 target/release/nebians --content .. --screenshots screenshots --reset`
(`scripts/screenshots.sh`). Signed-in screens use sample data — see LIMITATIONS.md.

**Live end-to-end hand-off test** (real Rust client ↔ real Django `runserver`, sqlite):
```
$ DB_ENGINE=sqlite DEBUG=True python manage.py runserver 127.0.0.1:8765 --noreload &
$ NEB_API_BASE=http://127.0.0.1:8765/ cargo test --release live_handoff -- --ignored --nocapture &
$ python scripts/e2e-handoff.py http://127.0.0.1:8765 <token of test user>
signed-out visitor is sent to login: /login/?next=/desktop-auth/%3Fstate%3D-BtnB65vVLBckCkOxRRJgX ...
consent page approved
--- cargo test output ---
SESSION user=e2e_tester is_new=false provider=browser
AUTHED unread-count reply: {"count":0}
test data::browser_auth::tests::live_handoff ... ok
```
The test additionally asserts that a bogus bearer token is rejected and that redeeming the same hand-off twice fails.

**Backend unit tests:** `DB_ENGINE=sqlite DEBUG=True SECRET_KEY=… python manage.py test api.test_desktop_auth` → `Ran 10 tests … OK`.

**Problems met and fixed this session:** Django needs `DB_ENGINE=sqlite` (default is MySQL) and `DEBUG=True` or a real `SECRET_KEY` to start; my first test of the device-name sanitiser expected parentheses to be stripped, but they're intentionally allowed (test corrected); `pkill -f` killed my own shell once (pattern matched the command line).
