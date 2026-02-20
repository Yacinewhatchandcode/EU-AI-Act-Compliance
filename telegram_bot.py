#!/usr/bin/env python3
"""
Prime-AI Telegram Bot — EU AI Act Compliance Scanner
=====================================================
Free distribution channel — no app store needed.
Users interact via Telegram to classify, scan, and audit AI systems.

Setup:
  1. Message @BotFather on Telegram
  2. Send /newbot → name it "Prime AI Compliance"
  3. Copy the token → set TELEGRAM_BOT_TOKEN env var
  4. Run: python telegram_bot.py
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import time
import threading
from pathlib import Path

# Add project dir
sys.path.insert(0, str(Path(__file__).parent))
from eu_ai_act import classify_ai_system, run_compliance_audit, generate_roadmap
from eu_ai_act_server import scan_url

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
API = f"https://api.telegram.org/bot{TOKEN}"
BOT_NAME = "Prime-AI Compliance Bot"


def tg(method: str, data: dict = None) -> dict:
    """Call Telegram Bot API."""
    url = f"{API}/{method}"
    if data:
        payload = json.dumps(data).encode()
        req = urllib.request.Request(url, data=payload,
                                     headers={"Content-Type": "application/json"})
    else:
        req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def send(chat_id: int, text: str, parse_mode: str = "Markdown",
         reply_markup: dict = None):
    """Send a message to a chat."""
    data = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}
    if reply_markup:
        data["reply_markup"] = reply_markup
    try:
        tg("sendMessage", data)
    except Exception as e:
        # Fallback without markdown if parsing fails
        data["parse_mode"] = None
        try:
            tg("sendMessage", data)
        except Exception:
            print(f"  ❌ Failed to send to {chat_id}: {e}")


def send_file(chat_id: int, file_path: str, caption: str = ""):
    """Send a file to a chat."""
    # For simplicity, use multipart form data via urllib
    import email.mime.multipart
    boundary = "----PrimeAIBoundary"
    body = []
    body.append(f"--{boundary}")
    body.append(f'Content-Disposition: form-data; name="chat_id"')
    body.append("")
    body.append(str(chat_id))
    body.append(f"--{boundary}")
    body.append(f'Content-Disposition: form-data; name="caption"')
    body.append("")
    body.append(caption)

    with open(file_path, "rb") as f:
        file_data = f.read()

    filename = os.path.basename(file_path)
    body.append(f"--{boundary}")
    body.append(f'Content-Disposition: form-data; name="document"; filename="{filename}"')
    body.append("Content-Type: application/octet-stream")
    body.append("")

    header_bytes = ("\r\n".join(body) + "\r\n").encode()
    footer_bytes = f"\r\n--{boundary}--\r\n".encode()
    full_body = header_bytes + file_data + footer_bytes

    req = urllib.request.Request(
        f"{API}/sendDocument",
        data=full_body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    urllib.request.urlopen(req, timeout=60)


# ═══════════════════════════════════════════════════════
# COMMAND HANDLERS
# ═══════════════════════════════════════════════════════

WELCOME = """🇪🇺 *Prime-AI — EU AI Act Compliance Bot*

I can help you check if your AI system complies with EU Regulation 2024/1689.

*Commands:*
🏷️ /classify `<description>` — Classify your AI system's risk level
🌐 /scan `<url>` — Scan any website for AI compliance
🔍 /audit `<system name>` — Run a compliance audit
🗺️ /roadmap `<system name>` — Generate a compliance roadmap
📊 /deadlines — View key EU AI Act deadlines
💡 /help — Show this menu

*Quick examples:*
• `/classify AI chatbot for customer service`
• `/scan https://openai.com`
• `/audit MyCompany HR Bot`

Powered by Prime-AI 🚀
"""

DEADLINES_TEXT = """📅 *EU AI Act Key Deadlines*

✅ *Feb 2, 2025* — Prohibited practices (Art. 5) in force
✅ *Aug 2, 2025* — GPAI rules applicable
⏳ *Aug 2, 2026* — High-risk obligations effective
📋 *Aug 2, 2027* — Annex I product rules

⚠️ Non-compliance penalties:
• 🔴 €35M or 7% global turnover (prohibited)
• 🟠 €15M or 3% (high-risk)
• 🟡 €7.5M or 1% (false information)
"""


def handle_start(chat_id, args):
    send(chat_id, WELCOME)


def handle_help(chat_id, args):
    send(chat_id, WELCOME)


def handle_classify(chat_id, args):
    if not args:
        send(chat_id, "⚠️ Please describe your AI system.\n\nExample:\n`/classify AI system that screens CVs for hiring decisions`")
        return

    description = " ".join(args)
    send(chat_id, f"🔄 Classifying: _{description}_...")

    result = classify_ai_system(description)
    level = result.get("risk_level", "unknown")

    if "prohibited" in level.lower():
        emoji = "🔴"
        badge = "PROHIBITED (BANNED IN EU)"
    elif "high" in level.lower():
        emoji = "🟠"
        badge = "HIGH RISK"
    elif "transparency" in str(result.get("transparency", "")) or result.get("article_50"):
        emoji = "🟡"
        badge = "LIMITED RISK (Transparency)"
    else:
        emoji = "🟢"
        badge = "MINIMAL / LOW RISK"

    reasons = result.get("reasons", [])
    reasons_text = "\n".join(f"  • {r}" for r in reasons) if reasons else "  • No specific flags"

    text = f"""{emoji} *Classification: {badge}*

📝 *Description:* {description}

📋 *Details:*
{reasons_text}

🔍 *Transparency (Art. 50):* {"Yes ✅" if result.get("transparency") else "No"}

💡 Use /audit to run a full compliance check.
"""
    send(chat_id, text)


def handle_scan(chat_id, args):
    if not args:
        send(chat_id, "⚠️ Please provide a URL to scan.\n\nExample:\n`/scan https://openai.com`")
        return

    url = args[0]
    if not url.startswith("http"):
        url = "https://" + url

    send(chat_id, f"🔄 Scanning _{url}_ for AI indicators...")

    result = scan_url(url)

    if result["status"] == "error":
        send(chat_id, f"❌ *Scan failed:* {result['summary']}")
        return

    level = result["risk_level"]
    if level == "HIGH":
        emoji = "🟠"
    elif level == "LIMITED":
        emoji = "🟡"
    elif level == "MINIMAL":
        emoji = "🟢"
    else:
        emoji = "⚪"

    indicators = result.get("ai_indicators", [])
    ind_text = ""
    for i in indicators[:8]:
        ind_text += f"\n  • *{i['category']}* — `{i['keyword']}` ×{i['count']} (W:{i['weight']})"

    obligations = result.get("obligations", [])
    obl_text = "\n".join(f"  • {o}" for o in obligations)

    text = f"""{emoji} *Scan Result: {level}*

🌐 *URL:* {url}
📊 *Score:* {result['score']} / {result['max_score']}
🔍 *Indicators found:* {len(indicators)}
{ind_text if ind_text else '  • None detected'}

📋 *Obligations:*
{obl_text}

_{result['summary']}_
"""
    send(chat_id, text)


def handle_audit(chat_id, args):
    system_name = " ".join(args) if args else "AI System"
    send(chat_id, f"🔄 Running compliance audit for _{system_name}_...")

    result = run_compliance_audit(system_name)
    pct = result.get("compliance_pct", 0)
    rating = result.get("rating", "?")

    if pct >= 90:
        emoji = "✅"
    elif pct >= 70:
        emoji = "⚠️"
    elif pct >= 50:
        emoji = "🟡"
    else:
        emoji = "❌"

    reqs = result.get("requirements", [])
    req_text = ""
    for r in reqs:
        status = r.get("status", "NOT_ASSESSED")
        st_icon = {"COMPLIANT": "✅", "PARTIAL": "⚠️", "NON_COMPLIANT": "❌"}.get(status, "⬜")
        req_text += f"\n  {st_icon} {r.get('name', r.get('id', '?'))} — {r.get('score', 0)}/{r.get('weight', r.get('w', 0))}"

    text = f"""{emoji} *Audit: {system_name}*

📊 *Compliance Score:* {pct}%
🏆 *Rating:* {rating}

📋 *Requirements (Art. 8-15):*
{req_text}

💡 Use /roadmap {system_name} to get an action plan.
"""
    send(chat_id, text)


def handle_roadmap(chat_id, args):
    system_name = " ".join(args) if args else "AI System"
    send(chat_id, f"🔄 Generating roadmap for _{system_name}_...")

    roadmap = generate_roadmap(system_name)
    # Truncate for Telegram (max 4096 chars)
    if len(roadmap) > 3500:
        roadmap = roadmap[:3500] + "\n\n... _(truncated — use web app for full roadmap)_"

    send(chat_id, f"🗺️ *Roadmap: {system_name}*\n\n```\n{roadmap}\n```")


def handle_deadlines(chat_id, args):
    send(chat_id, DEADLINES_TEXT)


COMMANDS = {
    "/start": handle_start,
    "/help": handle_help,
    "/classify": handle_classify,
    "/scan": handle_scan,
    "/audit": handle_audit,
    "/roadmap": handle_roadmap,
    "/deadlines": handle_deadlines,
}


# ═══════════════════════════════════════════════════════
# POLLING LOOP
# ═══════════════════════════════════════════════════════

def process_update(update: dict):
    """Process a single Telegram update."""
    msg = update.get("message", {})
    text = msg.get("text", "").strip()
    chat_id = msg.get("chat", {}).get("id")
    user = msg.get("from", {})

    if not chat_id or not text:
        return

    username = user.get("first_name", "User")
    print(f"  📩 [{username}] {text}")

    # Parse command
    parts = text.split()
    cmd = parts[0].lower().split("@")[0]  # Handle /command@botname
    args = parts[1:]

    handler = COMMANDS.get(cmd)
    if handler:
        try:
            handler(chat_id, args)
        except Exception as e:
            send(chat_id, f"❌ Error: {str(e)}")
            print(f"  ❌ Error handling {cmd}: {e}")
    elif text.startswith("/"):
        send(chat_id, f"❓ Unknown command: `{cmd}`\n\nSend /help for available commands.")
    else:
        # Free-text → auto-classify
        send(chat_id, f"💡 I'll classify that as an AI system description...")
        handle_classify(chat_id, parts)


def poll():
    """Long-polling loop for Telegram updates."""
    offset = 0
    print(f"\n  🤖 {BOT_NAME} is running!")
    print(f"  📱 Open Telegram and search for your bot\n")

    while True:
        try:
            result = tg("getUpdates", {"offset": offset, "timeout": 30})
            updates = result.get("result", [])

            for update in updates:
                offset = update["update_id"] + 1
                try:
                    process_update(update)
                except Exception as e:
                    print(f"  ❌ Update error: {e}")

        except KeyboardInterrupt:
            print("\n  Bot stopped.")
            break
        except Exception as e:
            print(f"  ⚠️ Poll error: {e}")
            time.sleep(5)


# ═══════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    if not TOKEN:
        print("""
╔══════════════════════════════════════════════════════════╗
║     🤖 Prime-AI Telegram Bot — Setup Required           ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  1. Open Telegram → search @BotFather                    ║
║  2. Send: /newbot                                        ║
║  3. Name: Prime-AI Compliance                            ║
║  4. Username: PrimeAI_bot (or similar)                   ║
║  5. Copy the API token                                   ║
║  6. Run:                                                 ║
║                                                          ║
║  $env:TELEGRAM_BOT_TOKEN = "YOUR_TOKEN_HERE"             ║
║  python telegram_bot.py                                  ║
║                                                          ║
║  That's it! Free, no app store, works everywhere.        ║
╚══════════════════════════════════════════════════════════╝
""")
        sys.exit(1)

    # Verify token
    try:
        me = tg("getMe")
        bot_info = me.get("result", {})
        print(f"""
╔══════════════════════════════════════════════════════════╗
║     🇪🇺 Prime-AI Telegram Bot — RUNNING                 ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  Bot:    @{bot_info.get('username', '?'):<48}║
║  Name:   {bot_info.get('first_name', '?'):<48}║
║  ID:     {bot_info.get('id', '?'):<48}║
║                                                          ║
║  Commands: /classify /scan /audit /roadmap /deadlines    ║
║  Free text → auto-classification                         ║
╚══════════════════════════════════════════════════════════╝
""")
    except Exception as e:
        print(f"❌ Invalid token: {e}")
        sys.exit(1)

    # Set bot commands for Telegram menu
    try:
        tg("setMyCommands", {"commands": [
            {"command": "classify", "description": "🏷️ Classify an AI system's risk level"},
            {"command": "scan", "description": "🌐 Scan any URL for AI compliance"},
            {"command": "audit", "description": "🔍 Run compliance audit"},
            {"command": "roadmap", "description": "🗺️ Generate compliance roadmap"},
            {"command": "deadlines", "description": "📅 EU AI Act key deadlines"},
            {"command": "help", "description": "💡 Show all commands"},
        ]})
    except Exception:
        pass

    poll()
