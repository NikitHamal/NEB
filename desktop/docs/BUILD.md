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
