$env:Path += ";C:\Program Files\nodejs;C:\Users\Mr Robot\AppData\Roaming\npm"
Write-Host "Logging out of WhatsApp to clear stale session..."
openclaw channels logout --channel whatsapp
Write-Host "Starting WhatsApp Login..."
openclaw channels login --channel whatsapp
Pause
