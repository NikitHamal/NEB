$infoPath = "F:\NEB\.ssh_deploy_info.json"
if (-not (Test-Path $infoPath)) {
    Write-Error "Deployment info file not found!"
    exit 1
}

$info = Get-Content $infoPath | ConvertFrom-Json
$hostIp = $info.host
$username = $info.username
$privateKey = $info.ssh_private_key

$keyPath = "$env:TEMP\nebians_tunnel_key.pem"
if (Test-Path $keyPath) {
    & icacls $keyPath /grant "${env:USERNAME}:F" 2>&1 | Out-Null
    attrib -r $keyPath 2>&1 | Out-Null
    Remove-Item $keyPath -Force -ErrorAction SilentlyContinue
}

$privateKey | Out-File -FilePath $keyPath -Encoding ascii -NoNewline
& icacls $keyPath /inheritance:r | Out-Null
& icacls $keyPath /grant "${env:USERNAME}:R" | Out-Null

$remoteScript = @"
echo "Killing old cloudflared processes..."
pkill -f "cloudflared tunnel"
sleep 1

echo "Starting fresh cloudflared quick tunnel..."
rm -f /tmp/cf_quick_active.log
nohup /home/consicac/.local/bin/cloudflared tunnel --no-autoupdate --protocol http2 --url http://127.0.0.1:8001 > /tmp/cf_quick_active.log 2>&1 &

sleep 4
echo "Checking log file /tmp/cf_quick_active.log..."
if [ -f /tmp/cf_quick_active.log ]; then
    cat /tmp/cf_quick_active.log
else
    echo "Log file not created!"
fi
"@

& ssh -o StrictHostKeyChecking=no -i $keyPath -p 22 "${username}@${hostIp}" $remoteScript

Remove-Item $keyPath -Force -ErrorAction SilentlyContinue
