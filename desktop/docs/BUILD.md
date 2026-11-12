# Building NEBians Desktop (v0.4.0)

Rust + egui/eframe 0.29 (glow). PDF rendering: `hayro` (pure Rust, CPU, no native DLLs).

## Windows .exe (cross-compiled from Linux — what is committed)
```
rustup target add x86_64-pc-windows-gnu
sudo apt-get install gcc-mingw-w64-x86-64
cd desktop
cargo build --release --target x86_64-pc-windows-gnu
# -> target/x86_64-pc-windows-gnu/release/nebians.exe
```
Committed binary: `desktop/releases/nebians-windows-x86_64.exe` (v0.4.0, ~19.4 MB, checksum in `SHA256SUMS`).
Native Windows: `cargo build --release` gives `target\release\nebians.exe`.

## Linux (used for the screenshot tour)
```
cargo build --release          # target/release/nebians
LIBGL_ALWAYS_SOFTWARE=1 xvfb-run -a -s "-screen 0 1280x800x24" \
  target/release/nebians --reset --config /tmp/neb-cfg --size 1280x800 --screenshots desktop/screenshots
```

## Flags
`nebians book.pdf` / `--open-pdf book.pdf` (needs a signed-in account), `--reset`, `--size WxH`, `--config DIR`, `--screenshots DIR`.

## Access
Only signed-in accounts reach the app: splash -> welcome tour (first run) -> sign in / create account -> profile setup -> home.
There is no guest mode. Account profile, security (email, password), privacy and terms, and account deletion are all native screens.
The single OS-browser step is Google/GitHub OAuth (providers refuse embedded web views); email sign-in is fully in-app.

## Viewer keys
PgUp/PgDn/Space scroll a screen, Home/End, Left/Right page, +/- zoom, W fit width, P fit page, T thumbnails, N night reading, Ctrl+wheel zoom, drag to pan.
