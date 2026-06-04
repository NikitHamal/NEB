param()
$info = Get-Content "F:\NEB\.ssh_deploy_info.json" | ConvertFrom-Json
$keyPath = "$env:TEMP\nebians_deploy_key_temp.pem"
$privateKey = $info.ssh_private_key
if (Test-Path $keyPath) {
    & icacls $keyPath /grant "${env:USERNAME}:F" 2>&1 | Out-Null
    attrib -r $keyPath 2>&1 | Out-Null
    Remove-Item $keyPath -Force -ErrorAction SilentlyContinue
}
$privateKey | Out-File -FilePath $keyPath -Encoding ascii -NoNewline
& icacls $keyPath /inheritance:r 2>&1 | Out-Null
& icacls $keyPath /grant "${env:USERNAME}:R" 2>&1 | Out-Null

# Use bash to call ssh with the remote command as a single arg
$remoteCmd = "cd /home/consicac/nebians_api && source /home/consicac/virtualenv/nebians_api/3.13/bin/activate && python -c 'from django.core.cache import cache; cache.delete(""admin_stats""); print(""Cache cleared"")'"
& ssh -o StrictHostKeyChecking=no -i $keyPath -p 22 "${info.username}@${info.host}" $remoteCmd

if (Test-Path $keyPath) {
    & icacls $keyPath /grant "${env:USERNAME}:F" 2>&1 | Out-Null
    attrib -r $keyPath 2>&1 | Out-Null
    Remove-Item $keyPath -Force -ErrorAction SilentlyContinue
}
