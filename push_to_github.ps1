# Prime-AI — Push to GitHub
# Run: .\push_to_github.ps1

Write-Host ""
Write-Host "  +====================================================+" -ForegroundColor Cyan
Write-Host "  |  PRIME-AI - GitHub Push                             |" -ForegroundColor Cyan
Write-Host "  +====================================================+" -ForegroundColor Cyan
Write-Host ""

$repoName = "EU-AI-Act-Compliance"
$githubUser = "Yacinewhatchandcode"
$remoteUrl = "https://github.com/$githubUser/$repoName.git"

# Check if git is configured
$email = git config user.email 2>$null
if (-not $email) {
    git config user.email "yacine@yace19ai.com"
    git config user.name "Yacinewhatchandcode"
}
Write-Host "  Git user: $(git config user.name) <$(git config user.email)>" -ForegroundColor Gray

# Set remote
$existingRemote = git remote get-url origin 2>$null
if ($existingRemote) {
    Write-Host "  Current remote: $existingRemote" -ForegroundColor Gray
    git remote set-url origin $remoteUrl
}
else {
    git remote add origin $remoteUrl
}
Write-Host "  Remote set: $remoteUrl" -ForegroundColor Green

# Stage all files
Write-Host ""
Write-Host "  Staging files..." -ForegroundColor Yellow
git add -A

# Show status
$status = git status --short | Measure-Object -Line
Write-Host "  $($status.Lines) files staged" -ForegroundColor Green

# Commit
$commitMsg = "feat: Prime-AI EU AI Act Compliance System

- Full-stack compliance toolkit for EU Regulation 2024/1689
- URL scanner, AI classifier (4 risk levels), 9-requirement audit
- PWA with Material Design 3 + auto JWT auth
- Multi-platform bots: Telegram, Slack, WhatsApp, Discord
- Marketing landing page with pricing
- Zero-config dev mode (auto-login, no setup needed)
- Complete regulatory database (Art. 5 prohibited + Annex III)
- Compliance reports, roadmaps, deadline tracking

By Yacine Benhamou | yace19ai.com"

git commit -m $commitMsg

# Push
Write-Host ""
Write-Host "  Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "  NOTE: You may be asked to authenticate." -ForegroundColor Yellow
Write-Host "  If using HTTPS, enter your GitHub Personal Access Token as password." -ForegroundColor Yellow
Write-Host ""

git branch -M main
git push -u origin main

Write-Host ""
Write-Host "  +====================================================+" -ForegroundColor Green
Write-Host "  |  DONE! Check: github.com/$githubUser/$repoName  |" -ForegroundColor Green
Write-Host "  +====================================================+" -ForegroundColor Green
