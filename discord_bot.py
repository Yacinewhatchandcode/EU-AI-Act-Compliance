#!/usr/bin/env python3
"""
Prime-AI Discord Bot — EU AI Act Compliance
=============================================
Free Discord server integration.

Setup:
  1. https://discord.com/developers/applications → New Application
  2. Name: "Prime-AI Compliance"
  3. Bot → Add Bot → copy token
  4. OAuth2 → URL Generator:
     - Scopes: bot, applications.commands
     - Permissions: Send Messages, Read Messages, Embed Links
  5. Copy invite URL → add to your server
  6. Run:
     $env:DISCORD_BOT_TOKEN = "your-token"
     python discord_bot.py
"""

import os
import sys
import json
import time
import urllib.request
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from bot_engine import handle_command

DISCORD_TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "")
DISCORD_API = "https://discord.com/api/v10"
HEARTBEAT_INTERVAL = 41250  # ms


def discord_api(method: str, path: str, data: dict = None) -> dict:
    """Call Discord REST API."""
    url = f"{DISCORD_API}{path}"
    headers = {
        "Authorization": f"Bot {DISCORD_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=payload, headers=headers,
                                 method=method)
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = resp.read()
        return json.loads(body) if body else {}


def send_message(channel_id: str, text: str):
    """Send a Discord message. Converts markdown for Discord."""
    # Discord uses **bold** instead of *bold*
    text = text.replace("*", "**")
    # Split if > 2000 chars
    chunks = [text[i:i+1900] for i in range(0, len(text), 1900)]
    for chunk in chunks:
        try:
            discord_api("POST", f"/channels/{channel_id}/messages",
                        {"content": chunk})
        except Exception as e:
            print(f"  ❌ Discord send error: {e}")


def process_message(data: dict):
    """Process a Discord MESSAGE_CREATE event."""
    # Ignore bot messages
    if data.get("author", {}).get("bot"):
        return

    content = data.get("content", "").strip()
    channel_id = data.get("channel_id", "")
    username = data.get("author", {}).get("username", "User")

    if not content or not channel_id:
        return

    # Only respond to commands or mentions
    # Check if message starts with / or ! or mentions the bot
    if not (content.startswith("/") or content.startswith("!") or
            content.startswith("prime") or content.lower().startswith("ai ")):
        return

    # Normalize command prefix
    if content.startswith("!"):
        content = "/" + content[1:]

    print(f"  📩 [Discord:{username}] {content}")

    result = handle_command(content, username)
    send_message(channel_id, result["text"])


# ═══════════════════════════════════════════════════════
# GATEWAY (WebSocket) — Pure Python, no dependencies
# ═══════════════════════════════════════════════════════

def gateway_connect():
    """Connect to Discord Gateway via WebSocket."""
    # We use a simple HTTP long-poll approach since we don't have
    # websocket library. For production, use discord.py.
    # Instead, we'll poll for messages using REST API.
    print("  ⚠️  Using REST polling mode (no websocket library)")
    print("  💡 For real-time: pip install discord.py")
    print()
    rest_poll()


def rest_poll():
    """Poll for new messages using REST API (fallback mode)."""
    # Get bot info
    me = discord_api("GET", "/users/@me")
    bot_id = me.get("id", "")
    print(f"  🤖 Bot: {me.get('username')}#{me.get('discriminator', '0')}")
    print(f"  🆔 ID: {bot_id}")

    # Get guilds
    guilds = discord_api("GET", "/users/@me/guilds")
    print(f"  🏠 Servers: {len(guilds)}")
    for g in guilds:
        print(f"     • {g['name']}")

    print(f"\n  📡 Listening for commands... (poll mode)")
    print(f"  💡 Users can type: /classify, /scan, /audit, /roadmap, /deadlines\n")

    # Track seen messages
    seen = set()
    channels_to_watch = []

    # Get text channels from each guild
    for guild in guilds:
        try:
            chs = discord_api("GET", f"/guilds/{guild['id']}/channels")
            for ch in chs:
                if ch.get("type") == 0:  # Text channel
                    channels_to_watch.append(ch["id"])
        except Exception:
            pass

    while True:
        for ch_id in channels_to_watch:
            try:
                messages = discord_api("GET", f"/channels/{ch_id}/messages?limit=5")
                for msg in messages:
                    msg_id = msg.get("id", "")
                    if msg_id in seen:
                        continue
                    seen.add(msg_id)

                    # Only process if it looks like a command
                    content = msg.get("content", "")
                    if content.startswith("/") or content.startswith("!"):
                        process_message(msg)

                # Limit seen set size
                if len(seen) > 10000:
                    seen.clear()

            except Exception:
                pass

        time.sleep(3)  # Poll every 3 seconds


# ═══════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("""
╔══════════════════════════════════════════════════════════╗
║     🎮 Prime-AI Discord Bot — Setup Required            ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  1. https://discord.com/developers/applications          ║
║  2. New Application → "Prime-AI Compliance"              ║
║  3. Bot → Add Bot → Copy Token                           ║
║  4. OAuth2 → URL Generator:                              ║
║     Scopes: bot, applications.commands                   ║
║     Permissions: Send/Read Messages, Embed Links         ║
║  5. Use invite URL to add bot to your server             ║
║  6. Run:                                                 ║
║                                                          ║
║  $env:DISCORD_BOT_TOKEN = "your-token"                   ║
║  python discord_bot.py                                   ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")
        sys.exit(1)

    # Verify token
    try:
        me = discord_api("GET", "/users/@me")
        print(f"""
╔══════════════════════════════════════════════════════════╗
║     🇪🇺 Prime-AI Discord Bot — RUNNING                  ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  Bot:    {me.get('username', '?'):<48}║
║  ID:     {me.get('id', '?'):<48}║
║                                                          ║
║  Commands: /classify /scan /audit /roadmap /deadlines    ║
║  Prefix:   / or !                                        ║
╚══════════════════════════════════════════════════════════╝
""")
    except Exception as e:
        print(f"❌ Invalid token: {e}")
        sys.exit(1)

    gateway_connect()
