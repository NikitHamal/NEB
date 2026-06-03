# Upload and run Ghostscript PDF compression on the server (Python version)

$infoPath = "F:\NEB\.ssh_deploy_info.json"
$info = Get-Content $infoPath | ConvertFrom-Json
$hostIp   = $info.host
$username = $info.username

# Write SSH key to temp file
$keyPath = "$env:TEMP\nebians_gs_key.pem"
if (Test-Path $keyPath) {
    & icacls $keyPath /grant "${env:USERNAME}:F" 2>&1 | Out-Null
    Remove-Item $keyPath -Force -ErrorAction SilentlyContinue
}
$info.ssh_private_key | Out-File -FilePath $keyPath -Encoding ascii -NoNewline
& icacls $keyPath /inheritance:r | Out-Null
& icacls $keyPath /grant "${env:USERNAME}:R" | Out-Null

$sshArgs = @("-o", "StrictHostKeyChecking=no", "-i", $keyPath, "-p", "22", "${username}@${hostIp}")
$scriptPath = Join-Path $PSScriptRoot "gs_compress_pdfs.sh"

# Upload the Python script
Write-Host "Uploading compression script..."
& scp -o StrictHostKeyChecking=no -i $keyPath -P 22 $scriptPath "${username}@${hostIp}:/tmp/gs_compress.py"
if ($LASTEXITCODE -ne 0) { Write-Error "SCP failed"; exit 1 }

# Run it using the virtualenv Python
Write-Host "Running Ghostscript compression on server..."
& ssh @sshArgs "/home/consicac/virtualenv/nebians_api/3.13/bin/python3 /tmp/gs_compress.py; rm -f /tmp/gs_compress.py"

# Cleanup local key
& icacls $keyPath /grant "${env:USERNAME}:F" 2>&1 | Out-Null
Remove-Item $keyPath -Force -ErrorAction SilentlyContinue
Write-Host "Done."
