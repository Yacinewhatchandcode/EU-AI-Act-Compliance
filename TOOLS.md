# TOOLS.md - OpenClaw Desktop Control Tools

## Desktop Control (PyAutoGUI)
Run from `C:\Users\Mr Robot\YBE\`:

```
python desktop_control.py <command> [args]
```

### Commands:
- `screenshot` — Take screenshot of full desktop, saves to `screenshot.png`
- `click <x> <y>` — Click at screen coordinates
- `double_click <x> <y>` — Double-click at coordinates
- `type <text>` — Type text with keyboard
- `hotkey <key1> <key2>` — Press key combo (e.g., `hotkey ctrl c`)
- `press <key>` — Press single key (enter, tab, escape, etc.)
- `move <x> <y>` — Move mouse to coordinates
- `scroll <amount>` — Scroll up (positive) or down (negative)
- `screen_size` — Get resolution (5120x2880)
- `mouse_pos` — Get current mouse position
- `find_window <title>` — Find and focus a window by title
- `open_app <command>` — Open any application

## Browser Research Tools
```
python browser_tools.py <command> [args]
```

### Commands:
- `perplexity [query]` — Open Perplexity AI (optional search query)
- `deep_search <query>` — Deep search with Perplexity, takes screenshot of results
- `chatgpt [message]` — Open ChatGPT (optional initial message)
- `ask_gpt <message>` — Send message to ChatGPT, wait for reply, screenshot
- `google <query>` — Google search with screenshot
- `open <url>` — Open any URL in Chrome

## Vercel Deployment
```
python deploy_vercel.py <project_dir>
```
Builds and deploys to Vercel staging. Returns the preview URL.

## Screen Info
- Resolution: 5120x2880 (5K display)
- OS: Windows

## Workflow: Full Autonomous Build
1. Receive idea on WhatsApp
2. `python browser_tools.py deep_search <research query>` — Research on Perplexity
3. `python browser_tools.py ask_gpt <question>` — Verify with ChatGPT if needed
4. Create project files using `write` tool
5. Run shell commands (npm, git, etc.)
6. `python desktop_control.py screenshot` — Verify visually
7. `python deploy_vercel.py <project_dir>` — Deploy to staging
8. Report staging URL back on WhatsApp

---
Add whatever helps you do your job. This is your cheat sheet.

## Prospect Finder (Lead Generation)
```
python prospect_finder.py <command> [args]
```

### Commands:
- `search` — Search ALL industries for prospects (real estate, beauty, hotels, etc.)
- `search real_estate` — Search specific industry only
- `sample` — Create sample CSV file for testing

Output: `prospects_YYYYMMDD_HHMM.csv` with columns: name;company;email;industry;city

## Email Campaign (PRIME.AI)
```
python email_campaign.py <command> [args]
```

### Commands:
- `send <prospects.csv>` — Send campaign to all prospects in CSV
- `test <email>` — Send single test email
- `preview` — Generate HTML preview and open in browser

### Workflow: Full Prospecting Pipeline
1. `python prospect_finder.py search` — Find prospects online
2. Review the CSV file, clean up if needed
3. `python email_campaign.py test info.primeai@gmail.com` — Test first
4. `python email_campaign.py send prospects.csv` — Launch campaign
5. Check `campaign_log.json` for results
