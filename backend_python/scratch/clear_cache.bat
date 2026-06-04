@echo off
set INFO=F:\NEB\.ssh_deploy_info.json
set KEY=%TEMP%\nebians_cache_key_temp.pem
if exist "%KEY%" del /F "%KEY%" 2>nul
for /f "delims=" %%a in ('powershell -Command "$info = Get-Content '%INFO%' | ConvertFrom-Json; Write-Output $info.ssh_private_key"') do set "PKEY=%%a"
echo %PKEY% > "%KEY%"
icacls "%KEY%" /inheritance:r >nul 2>&1
icacls "%KEY%" /grant "%USERNAME%:R" >nul 2>&1
for /f "delims=" %%b in ('powershell -Command "$info = Get-Content '%INFO%' | ConvertFrom-Json; Write-Output ('{0}@{1}' -f $info.username, $info.host)"') do set "DEST=%%b"
echo Cache clear starting...
ssh -o StrictHostKeyChecking=no -i "%KEY%" -p 22 "%DEST%" "cd /home/consicac/nebians_api && source /home/consicac/virtualenv/nebians_api/3.13/bin/activate && python -c 'from django.core.cache import cache; cache.delete(\"admin_stats\"); print(\"Cache cleared\")'"
icacls "%KEY%" /grant "%USERNAME%:F" >nul 2>&1
attrib -r "%KEY%" 2>nul
del /F "%KEY%" 2>nul
