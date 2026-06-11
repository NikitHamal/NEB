# Run remote test_qwen.py file to diagnose Qwen
$infoPath = "F:\NEB\.ssh_deploy_info.json"
if (-not (Test-Path $infoPath)) {
    Write-Error "Deployment info file not found!"
    exit 1
}

$info = Get-Content $infoPath | ConvertFrom-Json
$hostIp = $info.host
$username = $info.username
$privateKey = $info.ssh_private_key

$keyPath = "$env:TEMP\nebians_test2_key_temp.pem"
if (Test-Path $keyPath) {
    & icacls $keyPath /grant "${env:USERNAME}:F" 2>&1 | Out-Null
    attrib -r $keyPath 2>&1 | Out-Null
    Remove-Item $keyPath -Force -ErrorAction SilentlyContinue
}
$privateKey | Out-File -FilePath $keyPath -Encoding ascii -NoNewline
& icacls $keyPath /inheritance:r
& icacls $keyPath /grant "${env:USERNAME}:R"

# Create a small script content
$scriptContent = @'
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
django.setup()

from api.qwen_utils.client import QwenClient
import logging
logging.basicConfig(level=logging.INFO)

print("Starting QwenClient test...")
client = QwenClient()
res, err = client.simple_chat("Hello Qwen, are you there?")
print("Result:", res)
print("Error:", err)
'@

# Save locally to upload
$localTempScript = "f:\NEB\backend_python\scratch\test_qwen_temp.py"
$scriptContent | Out-File -FilePath $localTempScript -Encoding utf8

# Upload script via SCP
& scp -o StrictHostKeyChecking=no -i $keyPath -P 22 $localTempScript "${username}@${hostIp}:/home/consicac/nebians_api/test_qwen_temp.py"

# Run remote script
$runCmd = "cd /home/consicac/nebians_api && source /home/consicac/virtualenv/nebians_api/3.13/bin/activate && python test_qwen_temp.py && rm -f test_qwen_temp.py"
& ssh -o StrictHostKeyChecking=no -i $keyPath -p 22 "${username}@${hostIp}" $runCmd

# Cleanup local temp script
if (Test-Path $localTempScript) {
    Remove-Item $localTempScript -Force
}

if (Test-Path $keyPath) {
    & icacls $keyPath /grant "${env:USERNAME}:F" 2>&1 | Out-Null
    attrib -r $keyPath 2>&1 | Out-Null
    Remove-Item $keyPath -Force -ErrorAction SilentlyContinue
}
