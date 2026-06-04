$infoPath = "F:\NEB\.ssh_deploy_info.json"
if (-not (Test-Path $infoPath)) {
    Write-Error "Deployment info file not found!"
    exit 1
}

$info = Get-Content $infoPath | ConvertFrom-Json
$hostIp = $info.host
$username = $info.username
$privateKey = $info.ssh_private_key

$keyPath = "$env:TEMP\nebians_daphne_key.pem"
if (Test-Path $keyPath) {
    & icacls $keyPath /grant "${env:USERNAME}:F" 2>&1 | Out-Null
    attrib -r $keyPath 2>&1 | Out-Null
    Remove-Item $keyPath -Force -ErrorAction SilentlyContinue
}

$privateKey | Out-File -FilePath $keyPath -Encoding ascii -NoNewline
& icacls $keyPath /inheritance:r | Out-Null
& icacls $keyPath /grant "${env:USERNAME}:R" | Out-Null

function RunSSH($cmd) {
    & ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 -i $keyPath -p 22 "${username}@${hostIp}" $cmd
}

Write-Host "=== Stopping Daphne ==="
RunSSH "pkill -f 'daphne' 2>/dev/null; echo done"

Start-Sleep -Seconds 2

Write-Host "`n=== Stopping cloudflared ==="
RunSSH "pkill -f cloudflared 2>/dev/null; echo done"

Start-Sleep -Seconds 1

Write-Host "`n=== Starting Daphne ==="
RunSSH "source /home/consicac/virtualenv/nebians_api/3.13/bin/activate && cd /home/consicac/nebians_api && nohup daphne -b 127.0.0.1 -p 8001 nebians.asgi:application > /home/consicac/nebians_api/logs/daphne.log 2>&1 & sleep 3 && tail -n 5 /home/consicac/nebians_api/logs/daphne.log"

Write-Host "`n=== Starting cloudflared ==="
RunSSH "rm -f /tmp/cf_quick_active.log && nohup /home/consicac/.local/bin/cloudflared tunnel --no-autoupdate --protocol http2 --url http://127.0.0.1:8001 > /tmp/cf_quick_active.log 2>&1 & sleep 7 && grep -i trycloudflare /tmp/cf_quick_active.log | tail -3"

Remove-Item $keyPath -Force -ErrorAction SilentlyContinue
Write-Host "`nDone!"
