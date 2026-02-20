$env:Path = [System.Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path', 'User') + ";C:\Program Files\nodejs;C:\Users\Mr Robot\AppData\Roaming\npm"
Write-Host "Killing old processes..."
taskkill /F /IM node.exe 2>$null
Start-Sleep -Seconds 3
# Refresh environment variables to pick up FFmpeg and other changes
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
Write-Host "Refreshed PATH: $env:Path"

# Start the agent
openclaw gateway --profile main18789 --verbose
