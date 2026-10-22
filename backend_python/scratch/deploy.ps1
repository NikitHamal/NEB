# NEBians cPanel delta-based Deployment Script
# Optional: -TargetHost <ip> deploys to a different box with the same layout
# (e.g. the live box 202.63.243.186 instead of the default from .ssh_deploy_info.json).
#
# How it works (rewritten Oct 2026 - the old script streamed all ~61 MB on every
# deploy, 34 MB of which is the never-changing needle3.cact):
#   1. Hash the payload locally (relpath -> MD5) into a manifest.
#   2. Fetch .deploy_manifest.json from the server and diff it.
#   3. Zip + stream ONLY changed files (plus the new manifest) over the SSH exec
#      channel (the server kills SCP/SFTP). Removed files are deleted remotely.
#   4. pip install / collectstatic / migrate / Django check / daphne restart only
#      run when the relevant part of the tree actually changed.
#   5. LSAPI workers are recycled whenever anything changed.
param([string]$TargetHost = "")

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
if ($TargetHost -ne "") {
    $hostIp = $TargetHost
    Write-Host "Overriding target host: $hostIp"
}
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

$tempFiles = @()

function Remove-TempFiles {
    if (Test-Path $keyPath) {
        & icacls $keyPath /grant "${env:USERNAME}:F" 2>&1 | Out-Null
        attrib -r $keyPath 2>&1 | Out-Null
        Remove-Item $keyPath -Force -ErrorAction SilentlyContinue
    }
    foreach ($f in $tempFiles) {
        Remove-Item $f -Force -ErrorAction SilentlyContinue
    }
}

# --- 1. Build the local payload manifest (relpath -> MD5) ---------------------
Write-Host "Hashing payload files..."
$manifestPath = Join-Path $env:TEMP ("nebians_manifest_" + [guid]::NewGuid().ToString("N") + ".json")
$tempFiles += $manifestPath
Push-Location $projectDir
python -c @'
import os, json, hashlib, sys
out = sys.argv[1]
items = ['api', 'nebians', 'web', 'services', 'public', 'manage.py', 'requirements.txt', 'passenger_wsgi.py']
manifest = {}
def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()
for item in items:
    if os.path.isfile(item):
        manifest[item] = md5(item)
    elif os.path.isdir(item):
        for root, dirs, files in os.walk(item):
            dirs[:] = [d for d in dirs if d != '__pycache__']
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, '.').replace('\\', '/')
                if rel.endswith('.pyc'):
                    continue
                try:
                    manifest[rel] = md5(full)
                except Exception as e:
                    print(f'Warning skipping {full}: {e}')
with open(out, 'w') as fh:
    json.dump(manifest, fh, sort_keys=True)
print(f'MANIFEST files={len(manifest)}')
'@ $manifestPath
Pop-Location
if ($LASTEXITCODE -ne 0 -or -not (Test-Path $manifestPath)) {
    Write-Error "Failed to build the local payload manifest!"
    Remove-TempFiles
    exit 1
}
$localMap = @{}
(Get-Content $manifestPath -Raw | ConvertFrom-Json).PSObject.Properties | ForEach-Object { $localMap[$_.Name] = $_.Value }
Write-Host "Local manifest: $($localMap.Count) files"

# --- 2. Fetch the server-side manifest ----------------------------------------
Write-Host "Fetching server-side deploy manifest..."
$fetchScript = Join-Path $env:TEMP ("ssh_fetch_" + [guid]::NewGuid().ToString("N") + ".py")
$tempFiles += $fetchScript
@'
import subprocess, sys, time
key_path, target, remote_path = sys.argv[1], sys.argv[2], sys.argv[3]
host = target.split('@')[0] + '@' + target.split('@')[1].split(':')[0]
out = ''
for attempt in range(1, 4):
    try:
        r = subprocess.run(
            ['ssh', '-o', 'ConnectTimeout=30', '-o', 'StrictHostKeyChecking=no',
             '-i', key_path, '-p', '22', host, 'cat ' + remote_path + ' 2>/dev/null'],
            capture_output=True, timeout=60)
        out = r.stdout.decode('utf-8', 'replace')
        break
    except subprocess.TimeoutExpired:
        print(f'manifest fetch attempt {attempt} timed out', file=sys.stderr)
        time.sleep(3)
sys.stdout.write(out)
'@ | Out-File -FilePath $fetchScript -Encoding ascii -NoNewline
$remoteJson = (& python $fetchScript $keyPath "${username}@${hostIp}" "${remoteDir}/.deploy_manifest.json") -join "`n"
$remoteMap = @{}
if ($remoteJson -and $remoteJson.Trim().Length -gt 2) {
    try {
        ($remoteJson | ConvertFrom-Json).PSObject.Properties | ForEach-Object { $remoteMap[$_.Name] = $_.Value }
        Write-Host "Server manifest: $($remoteMap.Count) files"
    } catch {
        Write-Host "Server manifest unreadable - treating as empty (full upload)."
        $remoteMap = @{}
    }
} else {
    Write-Host "No server manifest yet - this deploy uploads the full payload."
}

# --- 3. Diff -------------------------------------------------------------------
$changed = @($localMap.Keys | Where-Object { $remoteMap[$_] -ne $localMap[$_] })
$deleted = @($remoteMap.Keys | Where-Object { -not $localMap.ContainsKey($_) })
$pyChanged = @($changed | Where-Object { $_ -match '\.py$' }).Count -gt 0
$reqChanged = $changed -contains 'requirements.txt'
$staticChanged = @($changed | Where-Object { $_ -like 'web/static/*' }).Count -gt 0
$staticDeleted = @($deleted | Where-Object { $_ -like 'web/static/*' }).Count -gt 0
$anyChanged = ($changed.Count -gt 0 -or $deleted.Count -gt 0)

Write-Host "Delta: $($changed.Count) changed, $($deleted.Count) removed (py=$pyChanged req=$reqChanged static=$staticChanged staticGone=$staticDeleted)"
if ($changed.Count -gt 0 -and $changed.Count -le 30) {
    $changed | Sort-Object | ForEach-Object { Write-Host "  ~ $_" }
}

# --- 4. Zip only the delta ------------------------------------------------------
$zipPath = Join-Path $env:TEMP ("nebians_deploy_" + [guid]::NewGuid().ToString("N") + ".zip")
$diffPath = Join-Path $env:TEMP ("nebians_diff_" + [guid]::NewGuid().ToString("N") + ".json")
$tempFiles += $zipPath, $diffPath
if ($anyChanged) {
    # WriteAllText (no BOM) - PowerShell 5.1's utf8 Set-Content adds a BOM that
    # breaks json.load() on the other side.
    [System.IO.File]::WriteAllText($diffPath, (@{ changed = $changed; deleted = $deleted } | ConvertTo-Json -Compress))
    Write-Host "Creating delta ZIP archive at $zipPath..."
    Push-Location $projectDir
    python -c @'
import json, sys, zipfile
zip_path, manifest_path, diff_path = sys.argv[1], sys.argv[2], sys.argv[3]
with open(manifest_path) as fh:
    manifest = json.load(fh)
with open(diff_path) as fh:
    diff = json.load(fh)
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for rel in diff['changed']:
        zf.write(rel, rel)
    # manifest lands atomically AFTER extraction (see remote script)
    zf.write(manifest_path, '.deploy_manifest.json.tmp')
    if diff['deleted']:
        zf.writestr('.deploy_delete.txt', '\n'.join(diff['deleted']) + '\n')
import os
print('DELTAZIP entries=' + str(len(diff['changed'])) + ' bytes=' + str(os.path.getsize(zip_path)))
'@ $zipPath $manifestPath $diffPath
    Pop-Location
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $zipPath)) {
        Write-Error "Failed to create the delta ZIP archive!"
        Remove-TempFiles
        exit 1
    }
}

# --- 5. Upload the delta ZIP (streamed over an SSH exec channel) ----------------
if ($anyChanged) {
    Write-Host "Uploading delta ZIP via SSH pipe..."
    $uploadScript = Join-Path $env:TEMP ("ssh_upload_" + [guid]::NewGuid().ToString("N") + ".py")
    $tempFiles += $uploadScript
    @'
import subprocess, sys
zip_path, key_path, target = sys.argv[1], sys.argv[2], sys.argv[3]
with open(zip_path, 'rb') as fh:
    data = fh.read()
for attempt in range(1, 6):
    r = subprocess.run(
        ['ssh', '-o', 'ConnectTimeout=30', '-o', 'ServerAliveInterval=15',
         '-o', 'ServerAliveCountMax=3', '-o', 'StrictHostKeyChecking=no',
         '-i', key_path, '-p', '22', target.split('@')[0] + '@' + target.split('@')[1].split(':')[0],
         'cat > ' + target.split(':', 1)[1]],
        input=data, capture_output=True, timeout=600)
    if r.returncode == 0:
        print(f'UPLOAD OK attempt={attempt} bytes={len(data)}')
        break
    print(f'UPLOAD attempt {attempt} failed rc={r.returncode}: {r.stderr.decode()[:200]}')
else:
    sys.exit(1)
'@ | Out-File -FilePath $uploadScript -Encoding ascii -NoNewline
    $uploadTarget = "${username}@${hostIp}:${remoteDir}/deploy.zip"
    & python $uploadScript $zipPath $keyPath $uploadTarget
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to upload delta ZIP after 5 attempts!"
        Remove-TempFiles
        exit 1
    }
    Remove-Item $uploadScript -Force -ErrorAction SilentlyContinue
    Write-Host "Delta ZIP upload completed."
}

# Upload the worker-restart script alongside (plain bash file - avoids PS escaping issues)
$restartLocal = Join-Path $PSScriptRoot "restart_workers.sh"
$uploadScript2 = Join-Path $env:TEMP ("ssh_upload_" + [guid]::NewGuid().ToString("N") + ".py")
$tempFiles += $uploadScript2
@'
import subprocess, sys
local_path, key_path, target = sys.argv[1], sys.argv[2], sys.argv[3]
with open(local_path, 'rb') as fh:
    data = fh.read()
r = subprocess.run(
    ['ssh', '-o', 'ConnectTimeout=10', '-o', 'StrictHostKeyChecking=no',
     '-i', key_path, '-p', '22', target.split('@')[0] + '@' + target.split('@')[1].split(':')[0],
     'cat > ' + target.split(':', 1)[1]],
    input=data, capture_output=True, timeout=60)
sys.exit(r.returncode)
'@ | Out-File -FilePath $uploadScript2 -Encoding ascii -NoNewline
& python $uploadScript2 $restartLocal $keyPath "${username}@${hostIp}:/tmp/restart_workers.sh" | Out-Null
Remove-Item $uploadScript2 -Force -ErrorAction SilentlyContinue

# --- 6. Build and run the remote deploy script (only the steps that are needed) --
Write-Host "--- Running Server-Side Deploy & Restart Commands ---"
$remote = New-Object System.Collections.Generic.List[string]
$remote.Add("cd $remoteDir")

if ($anyChanged) {
    $remote.Add("echo 'Extracting $($changed.Count) changed file(s)...'")
    $remote.Add("unzip -o deploy.zip >/dev/null && mv -f .deploy_manifest.json.tmp .deploy_manifest.json || { echo 'UNZIP FAILED'; exit 1; }")
    $remote.Add("rm -f deploy.zip")
    if ($deleted.Count -gt 0) {
        $remote.Add("echo 'Removing $($deleted.Count) retired file(s)...'")
        $remote.Add("xargs -d '\n' -r rm -f < .deploy_delete.txt")
        $remote.Add("rm -f .deploy_delete.txt")
    }
} else {
    $remote.Add("echo 'No file changes - payload already up to date.'")
    $remote.Add("rm -f deploy.zip .deploy_manifest.json.tmp")
}

if ($pyChanged) {
    $remote.Add("echo 'Clearing Python bytecode cache...'")
    $remote.Add("find . -name '*.pyc' -delete 2>/dev/null")
    $remote.Add("find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null")
    $remote.Add("echo 'Cache cleared.'")
}

$remote.Add("echo 'Removing retired files no longer shipped in the payload...'")
$remote.Add("rm -f api/ai4bharat_proxy.py")
$remote.Add("rm -f api/management/commands/arena_smoke_test.py")
$remote.Add("rm -f api/management/commands/arena_e2e_test.py")
$remote.Add("rm -f api/coding_agent/queue.py")
$remote.Add("echo 'Retired files cleaned.'")

$remote.Add("source /home/consicac/virtualenv/nebians_api/3.13/bin/activate")
$remote.Add("export OPENBLAS_NUM_THREADS=1")
$remote.Add("export OMP_NUM_THREADS=1")
$remote.Add("export MKL_NUM_THREADS=1")

if ($pyChanged) {
    $remote.Add("echo 'Sanity: Django check (catches missing/broken modules early)...'")
    $remote.Add("python manage.py check 2>&1 | tail -2 || echo 'WARNING: manage.py check reported issues'")
}

if ($reqChanged) {
    $remote.Add("echo 'Installing dependencies...'")
    $remote.Add("pip install -r requirements.txt")
}

if ($staticChanged -or $staticDeleted) {
    $clearFlag = ''
    if ($staticDeleted) { $clearFlag = '--clear' }
    $remote.Add("echo 'Running collectstatic...'")
    $remote.Add("python manage.py collectstatic --noinput $clearFlag")
}

if ($pyChanged) {
    $remote.Add("echo 'Running database migrations...'")
    $remote.Add("python manage.py migrate")
    $remote.Add("echo 'Backfilling video thumbnails...'")
    $remote.Add("python manage.py backfill_video_thumbnails || true")
}

# NOTE: WhiteNoise serves /static/ from staticfiles/ (verified), so the old
# public/static/web/* copies were dead weight (and errored on profile_art).
# Only the favicon copies remain - /favicon.ico is served from the docroot.
$remote.Add("echo 'Deploying favicon.ico to site root for /favicon.ico serving...'")
$remote.Add("cp -f web/static/web/img/favicon.ico public/favicon.ico")
$remote.Add("cp -f web/static/web/img/favicon.ico /home/consicac/nebians.consica.com.np/favicon.ico 2>/dev/null || true")

$remote.Add(@"
echo 'Resolving current WebSocket tunnel URL (newest mtime wins, ws_url.txt is fallback)...'
python3 << 'PYEOF'
import glob, re, os
candidates = []
paths = [
    '/home/consicac/nebians_api/logs/start_ws_tunnel.log',
    '/home/consicac/nebians_api/logs/cloudflared.log',
    'logs/cloudflared.log',
] + sorted(glob.glob('/tmp/cf_quick*.log'), reverse=True)
for p in paths:
    try:
        with open(p) as f:
            c = f.read()
        ms = re.findall(r'(?:wss?|https?)://([a-z0-9-]+\.trycloudflare\.com)', c)
        if ms:
            host = ms[-1]
            u = 'wss://' + host + '/ws/'
            try:
                mtime = os.path.getmtime(p)
            except:
                mtime = 0
            candidates.append((mtime, u, p))
    except Exception:
        continue
if candidates:
    candidates.sort(key=lambda x: x[0], reverse=True)
    u = candidates[0][1]
    src = candidates[0][2]
    with open('ws_url.txt', 'w') as wf:
        wf.write(u + '\n')
    print(f'WS URL: {u} (from {src} mtime={candidates[0][0]})')
else:
    try:
        with open('ws_url.txt') as f:
            c = f.read().strip()
        m = re.search(r'([a-z0-9-]+\.trycloudflare\.com)', c)
        if m:
            u = 'wss://' + m.group(1) + '/ws/'
            print(f'WS URL (fallback ws_url.txt): {u}')
        else:
            print('WARNING: could not resolve WS tunnel URL from logs or ws_url.txt')
    except Exception:
        print('WARNING: could not resolve WS tunnel URL')
    if not os.path.exists('ws_url.txt'):
        with open('ws_url.txt', 'w') as wf:
            wf.write('\n')
PYEOF
"@)

if ($pyChanged) {
    $remote.Add("echo 'Restarting background agent worker (autofix watcher removed Sep 2026)...'")
    $remote.Add("tr -d '\r' < /tmp/restart_workers.sh | bash")
}

if ($anyChanged) {
    $remote.Add("echo 'Restarting LSAPI workers (touch restart.txt alone does NOT recycle healthy workers)...'")
    # [i] bracket trick: the pattern must not match the remote shell running
    # this very script (its cmdline contains the pattern) or pkill kills the
    # SSH session itself - that silently ended every deploy at this line before.
    $remote.Add("pkill -f 'lswsgi -m ${remoteDir}/passenger_wsg[i].py' 2>/dev/null || true")
    $remote.Add("sleep 2")
}

$remote.Add("echo 'DEPLOYMENT SUCCESSFUL'")
$remoteScript = $remote -join "`n"

& ssh -o ConnectTimeout=30 -o ServerAliveInterval=15 -o ServerAliveCountMax=3 -o StrictHostKeyChecking=no -i $keyPath -p 22 "${username}@${hostIp}" $remoteScript
$sshExit = $LASTEXITCODE

Write-Host "Cleaning up temporary SSH key and ZIP files..."
Remove-TempFiles

if ($sshExit -ne 0) {
    Write-Error "Remote deploy commands failed (ssh exit=$sshExit). The payload may be partially deployed - re-run deploy.ps1 to converge."
    exit 1
}

Write-Host "Done!"
