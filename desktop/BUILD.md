# Building NEBians Desktop (v0.3.0)

Rust + egui/eframe 0.29 (glow). PDF rendering: `hayro` (pure Rust, CPU, no native DLLs).

## Windows .exe (cross-compiled from Linux, what is committed)
```
rustup target add x86_64-pc-windows-gnu
sudo apt-get install gcc-mingw-w64-x86-64
cd desktop
cargo build --release --target x86_64-pc-windows-gnu
# -> target/x86_64-pc-windows-gnu/release/nebians.exe
```
The committed binary is `desktop/releases/nebians-windows-x86_64.exe` (checksum in `SHA256SUMS`).
Native Windows: `cargo build --release` (MSVC or GNU toolchain) gives `target\release\nebians.exe`.

## Linux (used for screenshots)
```
cargo build --release          # target/release/nebians
LIBGL_ALWAYS_SOFTWARE=1 xvfb-run -a -s "-screen 0 1280x800x24" target/release/nebians --reset --size 1280x800 book.pdf
```

## Useful flags
`nebians book.pdf` / `--open-pdf book.pdf` opens straight into the in-app PDF viewer.
`--reset`, `--size WxH`, `--config DIR`, `--screenshots DIR` (scripted tour).

## Viewer keys
PgUp/PgDn/Space scroll a screen, Home/End, Left/Right page, +/- zoom, W fit width, P fit page,
T thumbnails, N night reading, Ctrl+wheel zoom, drag to pan.
