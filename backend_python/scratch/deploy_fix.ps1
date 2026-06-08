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

# Write SSH key to temp file
$keyPath = "$env:TEMP\nebians_deploy_fix_key.pem"
if (Test-Path $keyPath) {
    & icacls $keyPath /grant "${env:USERNAME}:F" 2>&1 | Out-Null
    attrib -r $keyPath 2>&1 | Out-Null
    Remove-Item $keyPath -Force -ErrorAction SilentlyContinue
}
Write-Host "Creating temporary SSH key file..."
$privateKey | Out-File -FilePath $keyPath -Encoding ascii -NoNewline

# Set correct SSH key permissions
Write-Host "Setting strict file permissions on the SSH key..."
& icacls $keyPath /inheritance:r | Out-Null
& icacls $keyPath /grant "${env:USERNAME}:R" | Out-Null

# Upload only the fixed middleware.py file
Write-Host "Uploading nebians/middleware.py to the server via SCP..."
& scp -o StrictHostKeyChecking=no -i $keyPath -P 22 "F:\NEB\backend_python\nebians\middleware.py" "${username}@${hostIp}:${remoteDir}/nebians/middleware.py"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to upload middleware.py!"
    Remove-Item $keyPath -Force
    exit 1
}
Write-Host "Upload completed successfully."

# Restart the application on the server
Write-Host "Restarting the application on the server..."
$restartCmd = "rm -rf ${remoteDir}/tmp/* && touch ${remoteDir}/tmp/restart.txt"
& ssh -o StrictHostKeyChecking=no -i $keyPath -p 22 "${username}@${hostIp}" $restartCmd

# Cleanup key
Write-Host "Cleaning up temporary SSH key file..."
Remove-Item $keyPath -Force -ErrorAction SilentlyContinue

Write-Host "DEPLOYMENT OF FIX SUCCESSFUL!"
