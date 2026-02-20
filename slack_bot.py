#!/usr/bin/env python3
"""
Prime-AI Slack Bot — EU AI Act Compliance
==========================================
Free Slack workspace integration.

Setup:
  1. Go to https://api.slack.com/apps → Create New App
  2. From Scratch → name "Prime-AI Compliance" → select workspace
  3. OAuth & Permissions → add scopes:
     - chat:write
     - commands
     - app_mentions:read
  4. Install to Workspace → copy Bot User OAuth Token
  5. Enable Socket Mode (or use Events API URL)
  6. Slash Commands → add /classify, /scan, /audit, /roadmap, /deadlines
  7. Run:
     $env:SLACK_BOT_TOKEN = "xoxb-your-token"
     $env:SLACK_APP_TOKEN = "xapp-your-token"  (for socket mode)
     python slack_bot.py
"""

import os
import sys
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from bot_engine import handle_command

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN", "")


def slack_api(method: str, data: dict = None) -> dict:
    """Call Slack Web API."""
    url = f"https://slack.com/api/{method}"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json; charset=utf-8",
    }
    payload = json.dumps(data or {}).encode()
    req = urllib.request.Request(url, data=payload, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def send_message(channel: str, text: str, thread_ts: str = None):
    """Send a Slack message."""
    # Convert markdown bold from *text* to Slack *text*  (same syntax, lucky)
    data = {"channel": channel, "text": text, "mrkdwn": True}
    if thread_ts:
        data["thread_ts"] = thread_ts
    result = slack_api("chat.postMessage", data)
    if not result.get("ok"):
        print(f"  ❌ Slack send error: {result.get('error', 'unknown')}")


def handle_slack_event(event: dict):
    """Process a Slack event."""
    event_type = event.get("type", "")

    if event_type == "app_mention" or event_type == "message":
        text = event.get("text", "").strip()
        channel = event.get("channel", "")
        user = event.get("user", "User")
        thread_ts = event.get("thread_ts") or event.get("ts")

        if not text or not channel:
            return

        # Remove bot mention from text: <@BOTID> /classify ...
        import re
        text = re.sub(r"<@[A-Z0-9]+>\s*", "", text).strip()

        if not text:
            text = "/help"

        print(f"  📩 [Slack:{user}] {text}")

        result = handle_command(text, user)
        send_message(channel, result["text"], thread_ts)


def handle_slash_command(payload: dict) -> str:
    """Handle a slash command from Slack."""
    command = payload.get("command", "").replace("/", "")
    text = payload.get("text", "")
    user = payload.get("user_name", "User")
    channel = payload.get("channel_id", "")

    full_text = f"/{command} {text}".strip()
    print(f"  📩 [Slack:{user}] {full_text}")

    result = handle_command(full_text, user)

    # For slash commands, we can respond immediately or post to channel
    if channel:
        send_message(channel, result["text"])

    return result["text"]


# ═══════════════════════════════════════════════════════
# SOCKET MODE (recommended for development)
# ═══════════════════════════════════════════════════════

def socket_mode_connect():
    """Connect via Slack Socket Mode (WebSocket)."""
    # Get WebSocket URL
    req = urllib.request.Request(
        "https://slack.com/api/apps.connections.open",
        data=b"",
        headers={"Authorization": f"Bearer {SLACK_APP_TOKEN}",
                 "Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())

    if not data.get("ok"):
        raise Exception(f"Socket Mode connect failed: {data.get('error')}")

    return data.get("url")


# ═══════════════════════════════════════════════════════
# HTTP MODE (for Events API — simpler without websocket)
# ═══════════════════════════════════════════════════════

import http.server


class SlackEventHandler(http.server.BaseHTTPRequestHandler):
    """Handle Slack Events API via HTTP."""

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode()

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            # Could be a slash command (form-encoded)
            data = dict(urllib.parse.parse_qsl(body))
            if "command" in data:
                result = handle_slash_command(data)
                self._respond(200, result)
                return
            self._respond(400, "Invalid request")
            return

        # URL verification challenge
        if data.get("type") == "url_verification":
            self._respond(200, data.get("challenge", ""), content_type="text/plain")
            return

        # Event callback
        if data.get("type") == "event_callback":
            event = data.get("event", {})
            # Ignore bot's own messages
            if event.get("bot_id"):
                self._respond(200, "ok")
                return
            # Process in background to respond quickly
            import threading
            threading.Thread(target=handle_slack_event, args=(event,), daemon=True).start()
            self._respond(200, "ok")
            return

        self._respond(200, "ok")

    def _respond(self, status, body, content_type="application/json"):
        if content_type == "application/json" and isinstance(body, str):
            body = json.dumps({"text": body})
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(body.encode() if isinstance(body, str) else body)

    def log_message(self, format, *args):
        pass  # Silence HTTP logs


def run_http_mode(port=3001):
    """Run Slack bot in HTTP Events API mode."""
    server = http.server.HTTPServer(("0.0.0.0", port), SlackEventHandler)
    print(f"  🌐 Slack Events API listening on port {port}")
    print(f"  📋 Set your Slack Events URL to: https://your-domain:{port}/")
    server.serve_forever()


# ═══════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    if not SLACK_BOT_TOKEN:
        print("""
╔══════════════════════════════════════════════════════════╗
║     🤖 Prime-AI Slack Bot — Setup Required              ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  1. Go to https://api.slack.com/apps                     ║
║  2. Create New App → From Scratch                        ║
║  3. Name: "Prime-AI Compliance"                          ║
║  4. OAuth & Permissions → Scopes:                        ║
║     • chat:write                                         ║
║     • commands                                           ║
║     • app_mentions:read                                  ║
║  5. Install to Workspace                                 ║
║  6. Copy Bot Token (xoxb-...)                            ║
║  7. Events → Subscribe to:                               ║
║     • app_mention                                        ║
║     • message.im                                         ║
║  8. Slash commands: /classify /scan /audit /deadlines     ║
║  9. Run:                                                 ║
║                                                          ║
║  $env:SLACK_BOT_TOKEN = "xoxb-your-token"                ║
║  python slack_bot.py                                     ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")
        sys.exit(1)

    # Verify token
    me = slack_api("auth.test")
    if not me.get("ok"):
        print(f"❌ Invalid token: {me.get('error')}")
        sys.exit(1)

    print(f"""
╔══════════════════════════════════════════════════════════╗
║     🇪🇺 Prime-AI Slack Bot — RUNNING                    ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  Bot:    {me.get('user', '?'):<48}║
║  Team:   {me.get('team', '?'):<48}║
║  URL:    {me.get('url', '?'):<48}║
║                                                          ║
║  Mode: HTTP Events API (port 3001)                       ║
║  Commands: /classify /scan /audit /roadmap /deadlines    ║
╚══════════════════════════════════════════════════════════╝
""")

    run_http_mode(3001)
