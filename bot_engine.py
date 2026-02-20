#!/usr/bin/env python3
"""
Prime-AI — Unified Multi-Platform Bot Engine
=============================================
One brain, many channels: Telegram, Slack, WhatsApp, Discord.
All platforms share this command handler.
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from eu_ai_act import classify_ai_system, run_compliance_audit, generate_roadmap
from eu_ai_act_server import scan_url


# ═══════════════════════════════════════════════════════
# SHARED COMMAND HANDLER — All platforms use this
# ═══════════════════════════════════════════════════════

def handle_command(text: str, user_name: str = "User") -> dict:
    """
    Process a command from any platform.
    Returns: {"text": str, "type": "text"|"file", "extra": dict}
    """
    text = text.strip()
    parts = text.split()
    cmd = parts[0].lower().replace("/", "").split("@")[0] if parts else ""
    args = parts[1:]

    handlers = {
        "start": cmd_start,
        "help": cmd_help,
        "classify": cmd_classify,
        "scan": cmd_scan,
        "audit": cmd_audit,
        "roadmap": cmd_roadmap,
        "deadlines": cmd_deadlines,
        "pricing": cmd_pricing,
    }

    handler = handlers.get(cmd)
    if handler:
        return handler(args, user_name)

    # If no command prefix, treat as free-text classification
    if not text.startswith("/"):
        return cmd_classify(parts, user_name)

    return {"text": f"❓ Unknown command: {cmd}\n\nSend /help for available commands.", "type": "text"}


# ═══════════════════════════════════════════════════════
# COMMANDS
# ═══════════════════════════════════════════════════════

def cmd_start(args, user):
    return {"text": f"""🇪🇺 *Prime-AI — EU AI Act Compliance*

Welcome {user}! I help you check AI compliance with EU Regulation 2024/1689.

*Commands:*
🏷️ /classify <description> — Risk classification
🌐 /scan <url> — Scan any website
🔍 /audit <system> — Compliance audit
🗺️ /roadmap <system> — Action plan
📅 /deadlines — Key dates
💰 /pricing — Our services

Or just describe your AI system and I'll classify it!

Powered by Prime-AI 🚀
""", "type": "text"}


def cmd_help(args, user):
    return cmd_start(args, user)


def cmd_classify(args, user):
    if not args:
        return {"text": "⚠️ Describe your AI system.\n\nExample: /classify AI chatbot for customer support", "type": "text"}

    description = " ".join(args)
    result = classify_ai_system(description)
    level = result.get("risk_level", "unknown")

    if "prohibited" in level.lower():
        emoji, badge = "🔴", "PROHIBITED"
    elif "high" in level.lower():
        emoji, badge = "🟠", "HIGH RISK"
    elif result.get("transparency") or result.get("article_50"):
        emoji, badge = "🟡", "LIMITED RISK"
    else:
        emoji, badge = "🟢", "MINIMAL RISK"

    reasons = result.get("reasons", [])
    reasons_text = "\n".join(f"  • {r}" for r in reasons) if reasons else "  • No specific concerns"

    return {"text": f"""{emoji} *{badge}*

📝 {description}

{reasons_text}

🔍 Transparency (Art. 50): {"Yes ✅" if result.get("transparency") else "No"}

💡 /audit to check all 9 requirements
""", "type": "text", "risk_level": level}


def cmd_scan(args, user):
    if not args:
        return {"text": "⚠️ Provide a URL.\n\nExample: /scan https://openai.com", "type": "text"}

    url = args[0]
    if not url.startswith("http"):
        url = "https://" + url

    result = scan_url(url)

    if result["status"] == "error":
        return {"text": f"❌ Scan failed: {result['summary']}", "type": "text"}

    level = result["risk_level"]
    emoji = {"HIGH": "🟠", "LIMITED": "🟡", "MINIMAL": "🟢"}.get(level, "⚪")

    indicators = result.get("ai_indicators", [])
    ind_text = ""
    for i in indicators[:6]:
        ind_text += f"\n  • *{i['category']}* — \"{i['keyword']}\" ×{i['count']}"

    obligations = "\n".join(f"  • {o}" for o in result.get("obligations", []))

    return {"text": f"""{emoji} *{level}*

🌐 {url}
📊 Score: {result['score']}/{result['max_score']} | {len(indicators)} indicators
{ind_text}

📋 *Obligations:*
{obligations}

_{result['summary']}_
""", "type": "text", "scan_result": result}


def cmd_audit(args, user):
    name = " ".join(args) if args else "AI System"
    result = run_compliance_audit(name)
    pct = result.get("compliance_pct", 0)

    emoji = "✅" if pct >= 90 else "⚠️" if pct >= 70 else "🟡" if pct >= 50 else "❌"

    reqs = result.get("requirements", [])
    req_text = ""
    for r in reqs:
        st = r.get("status", "NOT_ASSESSED")
        icon = {"COMPLIANT": "✅", "PARTIAL": "⚠️", "NON_COMPLIANT": "❌"}.get(st, "⬜")
        req_text += f"\n  {icon} {r.get('name', r.get('id', '?'))}"

    return {"text": f"""{emoji} *Audit: {name}* — {pct}%

{req_text}

💡 /roadmap {name} for action plan
""", "type": "text", "audit_result": result}


def cmd_roadmap(args, user):
    name = " ".join(args) if args else "AI System"
    roadmap = generate_roadmap(name)
    if len(roadmap) > 3500:
        roadmap = roadmap[:3500] + "\n\n... (use web app for full roadmap)"

    return {"text": f"🗺️ *Roadmap: {name}*\n\n```\n{roadmap}\n```", "type": "text"}


def cmd_deadlines(args, user):
    deadline = datetime(2026, 8, 2)
    days = (deadline - datetime.now()).days

    return {"text": f"""📅 *EU AI Act Deadlines* ({days} days remaining)

✅ *Feb 2025* — Prohibited practices (Art. 5)
✅ *Aug 2025* — GPAI rules
⏳ *Aug 2026* — High-risk obligations ({days}d)
📋 *Aug 2027* — Annex I products

⚠️ Penalties: up to €35M or 7% global turnover
""", "type": "text"}


def cmd_pricing(args, user):
    return {"text": """💰 *Prime-AI Services*

🆓 *Free* — Bot access (classify, scan, deadlines)
📋 *Starter — €49/mo*
  • Unlimited URL scans
  • Full compliance reports
  • Email support
🏢 *Business — €199/mo*
  • Everything in Starter
  • API access
  • Custom audits
  • Priority support
🏛️ *Enterprise — Custom*
  • On-premise deployment
  • Custom integrations
  • Dedicated account manager
  • SLA guarantees

📧 Contact: hello@prime-ai.eu
🌐 Web: prime-ai.eu
""", "type": "text"}
