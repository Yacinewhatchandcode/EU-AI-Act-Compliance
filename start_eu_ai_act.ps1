# Prime-AI - Master Launcher
# EU AI Act Compliance + Multi-Platform Bots

Write-Host ""
Write-Host "  +====================================================+" -ForegroundColor Cyan
Write-Host "  |     PRIME-AI - Full Stack Launcher                  |" -ForegroundColor Cyan
Write-Host "  +====================================================+" -ForegroundColor Cyan
Write-Host "  |                                                      |" -ForegroundColor Cyan
Write-Host "  |  [1] Web Server only  (port 8080)                   |" -ForegroundColor Cyan
Write-Host "  |  [2] ALL Bots         (Web + Telegram + Slack       |" -ForegroundColor Cyan
Write-Host "  |                        + WhatsApp + Discord)         |" -ForegroundColor Cyan
Write-Host "  |  [3] Telegram only                                   |" -ForegroundColor Cyan
Write-Host "  |  [4] Setup tokens     (configure all platforms)      |" -ForegroundColor Cyan
Write-Host "  |                                                      |" -ForegroundColor Cyan
Write-Host "  +====================================================+" -ForegroundColor Cyan
Write-Host ""

$choice = Read-Host "  Select option (1-4)"

switch ($choice) {
    "1" {
        Write-Host "`n  [WEB] Starting EU AI Act Web Server..." -ForegroundColor Green
        python "$PSScriptRoot\eu_ai_act_server.py"
    }
    "2" {
        Write-Host "`n  [ALL] Starting ALL configured bots..." -ForegroundColor Green
        python "$PSScriptRoot\start_all_bots.py"
    }
    "3" {
        if (-not $env:TELEGRAM_BOT_TOKEN) {
            Write-Host "`n  [!] TELEGRAM_BOT_TOKEN not set!" -ForegroundColor Yellow
            Write-Host "  1. Open Telegram, search @BotFather"
            Write-Host "  2. Send /newbot, name it Prime-AI Compliance"
            Write-Host "  3. Copy token and paste below:"
            Write-Host ""
            $token = Read-Host "  Paste your Telegram Bot Token"
            if ($token) {
                $env:TELEGRAM_BOT_TOKEN = $token
                Write-Host "  [OK] Token set!" -ForegroundColor Green
            }
        }
        python "$PSScriptRoot\telegram_bot.py"
    }
    "4" {
        Write-Host "`n  TOKEN SETUP" -ForegroundColor Cyan
        Write-Host "  -----------" -ForegroundColor DarkGray

        # Google OAuth
        Write-Host "`n  [GOOGLE OAUTH] (for web login):" -ForegroundColor Yellow
        if ($env:GOOGLE_CLIENT_ID -and $env:GOOGLE_CLIENT_ID -ne "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com") {
            $preview = $env:GOOGLE_CLIENT_ID.Substring(0, [Math]::Min(20, $env:GOOGLE_CLIENT_ID.Length))
            Write-Host "     [OK] Set: $preview..." -ForegroundColor Green
        }
        else {
            Write-Host "     [!] Not set" -ForegroundColor DarkYellow
            Write-Host "     Go to: https://console.cloud.google.com/apis/credentials"
            $t = Read-Host "     Paste Client ID (or Enter to skip)"
            if ($t) { $env:GOOGLE_CLIENT_ID = $t; Write-Host "     [OK] Set!" -ForegroundColor Green }
        }

        # Telegram
        Write-Host "`n  [TELEGRAM]:" -ForegroundColor Yellow
        if ($env:TELEGRAM_BOT_TOKEN) {
            Write-Host "     [OK] Set" -ForegroundColor Green
        }
        else {
            Write-Host "     [!] Not set - Talk to @BotFather on Telegram"
            $t = Read-Host "     Paste token (or Enter to skip)"
            if ($t) { $env:TELEGRAM_BOT_TOKEN = $t; Write-Host "     [OK] Set!" -ForegroundColor Green }
        }

        # Slack
        Write-Host "`n  [SLACK]:" -ForegroundColor Yellow
        if ($env:SLACK_BOT_TOKEN) {
            Write-Host "     [OK] Set" -ForegroundColor Green
        }
        else {
            Write-Host "     [!] Not set - Go to: https://api.slack.com/apps"
            $t = Read-Host "     Paste token (or Enter to skip)"
            if ($t) { $env:SLACK_BOT_TOKEN = $t; Write-Host "     [OK] Set!" -ForegroundColor Green }
        }

        # WhatsApp
        Write-Host "`n  [WHATSAPP]:" -ForegroundColor Yellow
        if ($env:WHATSAPP_TOKEN) {
            Write-Host "     [OK] Set" -ForegroundColor Green
        }
        else {
            Write-Host "     [!] Not set - Go to: https://developers.facebook.com"
            $t = Read-Host "     Paste token (or Enter to skip)"
            if ($t) { $env:WHATSAPP_TOKEN = $t; Write-Host "     [OK] Set!" -ForegroundColor Green }
            $p = Read-Host "     Phone Number ID (or Enter to skip)"
            if ($p) { $env:WHATSAPP_PHONE_ID = $p; Write-Host "     [OK] Phone ID set!" -ForegroundColor Green }
        }

        # Discord
        Write-Host "`n  [DISCORD]:" -ForegroundColor Yellow
        if ($env:DISCORD_BOT_TOKEN) {
            Write-Host "     [OK] Set" -ForegroundColor Green
        }
        else {
            Write-Host "     [!] Not set - Go to: https://discord.com/developers/applications"
            $t = Read-Host "     Paste token (or Enter to skip)"
            if ($t) { $env:DISCORD_BOT_TOKEN = $t; Write-Host "     [OK] Set!" -ForegroundColor Green }
        }

        Write-Host "`n  Setup complete! Launching all bots..." -ForegroundColor Green
        Start-Sleep 1
        python "$PSScriptRoot\start_all_bots.py"
    }
    default {
        Write-Host "  Starting web server by default..." -ForegroundColor DarkGray
        python "$PSScriptRoot\eu_ai_act_server.py"
    }
}
