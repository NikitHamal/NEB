# NEBians cPanel ZIP-based Deployment Script

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectDir = Split-Path -Parent $scriptDir

$infoPath = "F:\NEB\.ssh_deploy_info.json"
if (-not (Test-Path $infoPath)) {
    Write-Error "Deployment info file not found!"
    exit 1
}

Write-Host "Reading deployment configuration..."
$info = Get-Content $infoPath | ConvertFrom-Json
$hostIp = $info.host
$username = $info.username
$remoteDir = $info.remote_project_dir
$privateKey = $info.ssh_private_key

# Write SSH key to temp file
$keyPath = "$env:TEMP\nebians_deploy_key_temp.pem"
if (Test-Path $keyPath) {
    & icacls $keyPath /grant "${env:USERNAME}:F" 2>&1 | Out-Null
    attrib -r $keyPath 2>&1 | Out-Null
    Remove-Item $keyPath -Force -ErrorAction SilentlyContinue
}
Write-Host "Creating temporary SSH key file at: $keyPath"
$privateKey | Out-File -FilePath $keyPath -Encoding ascii -NoNewline

# Set correct SSH key permissions
Write-Host "Setting strict file permissions on the SSH key..."
& icacls $keyPath /inheritance:r
& icacls $keyPath /grant "${env:USERNAME}:R"

# Create a local zip archive of deployment files
$zipPath = Join-Path $projectDir "deploy.zip"
if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
}
Write-Host "Creating local ZIP archive of deployment files..."
Push-Location $projectDir
Compress-Archive -Path api, nebians, web, manage.py, requirements.txt, passenger_wsgi.py -DestinationPath $zipPath -Force
Pop-Location

# Upload the ZIP file
Write-Host "Uploading ZIP file via SCP..."
& scp -o StrictHostKeyChecking=no -i $keyPath -P 22 $zipPath "${username}@${hostIp}:${remoteDir}/"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to upload ZIP archive!"
    Remove-Item $keyPath -Force
    Remove-Item $zipPath -Force -ErrorAction SilentlyContinue
    exit 1
}
Write-Host "ZIP upload completed successfully."

# Remove local zip archive
Remove-Item $zipPath -Force

# Remote commands to unzip and deploy
Write-Host "--- Running Server-Side Deploy & Restart Commands ---"
$remoteScript = @"
cd ${remoteDir}

echo 'Unzipping deployment files...'
unzip -o deploy.zip
rm -f deploy.zip

source /home/consicac/virtualenv/nebians_api/3.13/bin/activate

echo 'Installing dependencies...'
pip install -r requirements.txt

echo 'Running collectstatic...'
python manage.py collectstatic --noinput

echo 'Running database migrations...'
python manage.py migrate

echo 'Resolving cPanel static files two-location copies...'
mkdir -p public/static/web/css
mkdir -p public/static/web/js
mkdir -p public/static/web/img
cp -f web/static/web/css/app.css public/static/web/css/app.css
cp -f web/static/web/css/material3.css public/static/web/css/material3.css
cp -f web/static/web/css/admin.css public/static/web/css/admin.css
cp -f web/static/web/js/delegated-events.js public/static/web/js/delegated-events.js
cp -f web/static/web/js/marked.min.js public/static/web/js/marked.min.js
cp -f web/static/web/js/realtime.js public/static/web/js/realtime.js
cp -f web/static/web/manifest.json public/static/web/manifest.json
cp -rf web/static/web/img/ public/static/web/img/

echo 'Restarting Phusion Passenger application...'
rm -rf tmp/*
touch tmp/restart.txt

echo 'DEPLOYMENT SUCCESSFUL'
"@

# Execute remote script via SSH
& ssh -o StrictHostKeyChecking=no -i $keyPath -p 22 "${username}@${hostIp}" $remoteScript

# Cleanup key
Write-Host "Cleaning up temporary SSH key file..."
if (Test-Path $keyPath) {
    & icacls $keyPath /grant "${env:USERNAME}:F" 2>&1 | Out-Null
    attrib -r $keyPath 2>&1 | Out-Null
    Remove-Item $keyPath -Force -ErrorAction SilentlyContinue
}

Write-Host "Done!"
