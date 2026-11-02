# Native Windows build (PowerShell). Requires Rust (https://rustup.rs) with the MSVC toolchain.
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")
cargo build --release
Get-Item target\release\nebians.exe | Select-Object Name, Length
Write-Host "Run:  target\release\nebians.exe --content <path-to-NEB-checkout>"
