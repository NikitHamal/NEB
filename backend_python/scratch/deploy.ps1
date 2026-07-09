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
# Clean local __pycache__ before zipping
Get-ChildItem -Path api, nebians, web, services -Directory -Recurse -Filter '__pycache__' -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

Compress-Archive -Path api, nebians, web, services, public, manage.py, requirements.txt, passenger_wsgi.py -DestinationPath $zipPath -Force
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

echo 'Clearing Python bytecode cache...'
find . -name '*.pyc' -delete 2>/dev/null
find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null
echo 'Cache cleared.'

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
cp -rf web/static/web/css/* public/static/web/css/
cp -rf web/static/web/js/* public/static/web/js/
cp -f web/static/web/manifest.json public/static/web/manifest.json
cp -rf web/static/web/img/* public/static/web/img/

echo 'Deploying favicon.ico to site root for /favicon.ico serving...'
cp -f web/static/web/img/favicon.ico public/favicon.ico

echo 'Deploying .htaccess security rules...'
cp -f public/.htaccess public/.htaccess

echo 'Resolving current WebSocket tunnel URL...'
python3 << 'PYEOF'
import glob, re, os
paths = sorted(glob.glob('/tmp/cf_quick*.log'), reverse=True) + ['/home/consicac/nebians_api/logs/cloudflared.log']
for p in paths:
    try:
        with open(p) as f:
            c = f.read()
        m = re.search(r'https://([a-z0-9-]+\.trycloudflare\.com)', c)
        if m:
            u = 'wss://' + m.group(1) + '/ws/'
            with open('ws_url.txt', 'w') as wf:
                wf.write(u + '\n')
            print('WS URL:', u)
            break
    except Exception:
        continue
else:
    print('WARNING: could not resolve WS tunnel URL')
    if not os.path.exists('ws_url.txt'):
        with open('ws_url.txt', 'w') as wf:
            wf.write('\n')
PYEOF

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
