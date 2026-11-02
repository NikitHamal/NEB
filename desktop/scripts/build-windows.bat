@echo off
rem Native Windows build. Requires Rust (https://rustup.rs).
cd /d "%~dp0.."
cargo build --release || exit /b 1
dir target\release\nebians.exe
echo Run:  target\release\nebians.exe --content ^<path-to-NEB-checkout^>
