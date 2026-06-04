$keyPath = "C:\Users\Acer\AppData\Local\Temp\nebians_deploy_key_temp.pem"
$info = Get-Content -LiteralPath "F:\NEB\.ssh_deploy_info.json" -Raw | ConvertFrom-Json

if (Test-Path $keyPath) {
    icacls $keyPath /grant "${env:USERNAME}:F" 2>&1 | Out-Null
    attrib -r $keyPath 2>&1 | Out-Null
    Remove-Item $keyPath -Force -ErrorAction SilentlyContinue
}

$info.ssh_private_key | Out-File -FilePath $keyPath -Encoding ascii -NoNewline

icacls $keyPath /inheritance:r 2>&1 | Out-Null
icacls $keyPath /grant "${env:USERNAME}:R" 2>&1 | Out-Null

Write-Output "Key ready: $keyPath"
Get-Acl $keyPath | Format-List