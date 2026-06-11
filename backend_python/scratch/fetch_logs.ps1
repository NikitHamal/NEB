# Fetch logs from remote server
$infoPath = "F:\NEB\.ssh_deploy_info.json"
if (-not (Test-Path $infoPath)) {
    Write-Error "Deployment info file not found!"
    exit 1
}

$info = Get-Content $infoPath | ConvertFrom-Json
$hostIp = $info.host
$username = $info.username
$remoteDir = $info.remote_project_dir
$privateKey = $info.ssh_private_key

$keyPath = "$env:TEMP\nebians_fetch_key_temp.pem"
if (Test-Path $keyPath) {
    & icacls $keyPath /grant "${env:USERNAME}:F" 2>&1 | Out-Null
    attrib -r $keyPath 2>&1 | Out-Null
    Remove-Item $keyPath -Force -ErrorAction SilentlyContinue
}
$privateKey | Out-File -FilePath $keyPath -Encoding ascii -NoNewline
& icacls $keyPath /inheritance:r
& icacls $keyPath /grant "${env:USERNAME}:R"

Write-Host "=== Fetching nebians.log ==="
& ssh -o StrictHostKeyChecking=no -i $keyPath -p 22 "${username}@${hostIp}" "tail -n 150 /home/consicac/nebians_api/logs/nebians.log"

Write-Host "`n=== Fetching cPanel error_log ==="
& ssh -o StrictHostKeyChecking=no -i $keyPath -p 22 "${username}@${hostIp}" "tail -n 150 /home/consicac/logs/error_log"

if (Test-Path $keyPath) {
    & icacls $keyPath /grant "${env:USERNAME}:F" 2>&1 | Out-Null
    attrib -r $keyPath 2>&1 | Out-Null
    Remove-Item $keyPath -Force -ErrorAction SilentlyContinue
}
