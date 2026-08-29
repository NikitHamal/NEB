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

# Create a local zip archive of deployment files in TEMP
$zipPath = Join-Path $env:TEMP ("nebians_deploy_" + [guid]::NewGuid().ToString("N") + ".zip")
if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force -ErrorAction SilentlyContinue
}
Write-Host "Creating local ZIP archive of deployment files at $zipPath..."
Push-Location $projectDir

python -c "
import os, zipfile, sys
zip_path = sys.argv[1]
items = ['api', 'nebians', 'web', 'services', 'public', 'manage.py', 'requirements.txt', 'passenger_wsgi.py']
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for item in items:
        if os.path.isfile(item):
            zf.write(item, item)
        elif os.path.isdir(item):
            for root, dirs, files in os.walk(item):
                dirs[:] = [d for d in dirs if d != '__pycache__']
                for f in files:
                    full = os.path.join(root, f)
                    rel = os.path.relpath(full, '.')
                    try:
                        zf.write(full, rel)
                    except Exception as e:
                        print(f'Warning skipping {full}: {e}')
" "$zipPath"

Pop-Location

# Upload the ZIP file
Write-Host "Uploading ZIP file via SCP..."
$uploadSuccess = $false
for ($attempt = 1; $attempt -le 5; $attempt++) {
    & scp -o ConnectTimeout=30 -o ServerAliveInterval=15 -o ServerAliveCountMax=3 -o StrictHostKeyChecking=no -i $keyPath -P 22 $zipPath "${username}@${hostIp}:${remoteDir}/deploy.zip"
    if ($LASTEXITCODE -eq 0) {
        $uploadSuccess = $true
        break
    }
    Write-Host "SCP upload attempt $attempt failed, retrying in 4 seconds..."
    Start-Sleep -Seconds 4
}

if (-not $uploadSuccess) {
    Write-Error "Failed to upload ZIP archive after 3 attempts!"
    & icacls $keyPath /grant "${env:USERNAME}:F" 2>&1 | Out-Null
    attrib -r $keyPath 2>&1 | Out-Null
    Remove-Item $keyPath -Force -ErrorAction SilentlyContinue
    Remove-Item $zipPath -Force -ErrorAction SilentlyContinue
    exit 1
}
Write-Host "ZIP upload completed successfully."

# Upload the worker-restart script alongside (plain bash file — avoids PS escaping issues)
& scp -o ConnectTimeout=10 -o StrictHostKeyChecking=no -i $keyPath -P 22 (Join-Path $PSScriptRoot "restart_workers.sh") "${username}@${hostIp}:/tmp/restart_workers.sh" | Out-Null

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

echo 'Removing retired files no longer shipped in the ZIP...'
rm -f api/ai4bharat_proxy.py
rm -f api/management/commands/arena_smoke_test.py
rm -f api/management/commands/arena_e2e_test.py
rm -f api/coding_agent/queue.py
echo 'Retired files cleaned.'

source /home/consicac/virtualenv/nebians_api/3.13/bin/activate
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1

echo 'Sanity: Django check (catches missing/broken modules early)...'
python manage.py check 2>&1 | tail -2 || echo 'WARNING: manage.py check reported issues'

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
cp -f web/static/web/img/favicon.ico /home/consicac/nebians.consica.com.np/favicon.ico 2>/dev/null || true

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

echo 'Backfilling video thumbnails...'
python manage.py backfill_video_thumbnails || true



echo 'Restarting background agent worker and autofix watcher...'
tr -d '\r' < /tmp/restart_workers.sh | bash

echo 'Restarting LSAPI workers (touch restart.txt alone does NOT recycle healthy workers)...'
pkill -f 'lswsgi -m ${remoteDir}/passenger_wsgi.py' 2>/dev/null || true
sleep 2

echo 'DEPLOYMENT SUCCESSFUL'
"@

# Execute remote script via SSH
& ssh -o ConnectTimeout=30 -o ServerAliveInterval=15 -o ServerAliveCountMax=3 -o StrictHostKeyChecking=no -i $keyPath -p 22 "${username}@${hostIp}" $remoteScript

# Cleanup key and temp zip
Write-Host "Cleaning up temporary SSH key and ZIP files..."
if (Test-Path $keyPath) {
    & icacls $keyPath /grant "${env:USERNAME}:F" 2>&1 | Out-Null
    attrib -r $keyPath 2>&1 | Out-Null
    Remove-Item $keyPath -Force -ErrorAction SilentlyContinue
}
if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force -ErrorAction SilentlyContinue
}

Write-Host "Done!"
