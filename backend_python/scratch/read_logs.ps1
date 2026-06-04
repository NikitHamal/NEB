$infoPath = "F:\NEB\.ssh_deploy_info.json"
if (-not (Test-Path $infoPath)) {
    Write-Error "Deployment info file not found!"
    exit 1
}

$info = Get-Content $infoPath | ConvertFrom-Json
$hostIp = $info.host
$username = $info.username
$privateKey = $info.ssh_private_key

$keyPath = "$env:TEMP\nebians_read_logs_key.pem"
if (Test-Path $keyPath) {
    & icacls $keyPath /grant "${env:USERNAME}:F" 2>&1 | Out-Null
    attrib -r $keyPath 2>&1 | Out-Null
    Remove-Item $keyPath -Force -ErrorAction SilentlyContinue
}

$privateKey | Out-File -FilePath $keyPath -Encoding ascii -NoNewline
& icacls $keyPath /inheritance:r | Out-Null
& icacls $keyPath /grant "${env:USERNAME}:R" | Out-Null

Write-Host "--- Active Cloudflare Tunnel Log ---"
& ssh -o StrictHostKeyChecking=no -i $keyPath -p 22 "${username}@${hostIp}" "cat /tmp/cf_quick_active.log"

Write-Host "`n--- Daphne Log ---"
& ssh -o StrictHostKeyChecking=no -i $keyPath -p 22 "${username}@${hostIp}" "tail -n 25 /home/consicac/nebians_api/logs/daphne.log"

Write-Host "`n--- Django App Log ---"
& ssh -o StrictHostKeyChecking=no -i $keyPath -p 22 "${username}@${hostIp}" "tail -n 25 /home/consicac/nebians_api/logs/nebians.log"

Remove-Item $keyPath -Force -ErrorAction SilentlyContinue
