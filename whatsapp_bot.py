#!/usr/bin/env python3
"""
Prime-AI WhatsApp Bot — EU AI Act Compliance
==============================================
Uses WhatsApp Business Cloud API (Meta).
Works alongside existing OpenClaw WhatsApp integration.

Setup:
  1. Go to https://developers.facebook.com → Create App → Business
  2. Add WhatsApp product
  3. Get a test phone number + token from the dashboard
  4. Set webhook URL to https://your-domain:3002/webhook
  5. Subscribe to "messages" webhook field
  6. Run:
     $env:WHATSAPP_TOKEN = "your-token"
     $env:WHATSAPP_PHONE_ID = "your-phone-number-id"
     $env:WHATSAPP_VERIFY_TOKEN = "your-custom-verify-string"
     python whatsapp_bot.py
"""

import os
import sys
import json
import http.server
import urllib.request
import urllib.parse
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from bot_engine import handle_command

WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN", "")
WHATSAPP_PHONE_ID = os.environ.get("WHATSAPP_PHONE_ID", "")
WHATSAPP_VERIFY_TOKEN = os.environ.get("WHATSAPP_VERIFY_TOKEN", "primeai-verify-2026")
GRAPH_API = "https://graph.facebook.com/v19.0"

PORT = int(os.environ.get("WHATSAPP_PORT", 3002))


def wa_send(to: str, text: str):
    """Send a WhatsApp text message via Cloud API."""
    url = f"{GRAPH_API}/{WHATSAPP_PHONE_ID}/messages"
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {"preview_url": False, "body": text},
    }
    payload = json.dumps(data).encode()
    req = urllib.request.Request(url, data=payload, headers={
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())
            if "messages" in result:
                print(f"  ✅ Sent to {to}")
            return result
    except Exception as e:
        print(f"  ❌ WhatsApp send error: {e}")
        return None


def wa_mark_read(message_id: str):
    """Mark a message as read."""
    url = f"{GRAPH_API}/{WHATSAPP_PHONE_ID}/messages"
    data = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id,
    }
    try:
        payload = json.dumps(data).encode()
        req = urllib.request.Request(url, data=payload, headers={
            "Authorization": f"Bearer {WHATSAPP_TOKEN}",
            "Content-Type": "application/json",
        })
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass


def process_whatsapp_message(message: dict, contact: dict):
    """Process an incoming WhatsApp message."""
    msg_type = message.get("type", "")
    msg_id = message.get("id", "")
    sender = message.get("from", "")
    name = contact.get("profile", {}).get("name", sender)

    if msg_type != "text":
        wa_send(sender, "I can only process text messages for now.\n\nSend /help for commands.")
        return

    text = message.get("text", {}).get("body", "").strip()
    if not text:
        return

    print(f"  📩 [WhatsApp:{name}] {text}")

    # Mark as read
    wa_mark_read(msg_id)

    # Process command
    result = handle_command(text, name)

    # WhatsApp has a 4096 char limit per message
    response = result["text"]
    # Convert Markdown bold (*text*) — WhatsApp uses *text* natively!
    # Convert code blocks
    response = response.replace("```", "")

    if len(response) > 4000:
        # Split into chunks
        chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
        for chunk in chunks:
            wa_send(sender, chunk)
    else:
        wa_send(sender, response)


# ═══════════════════════════════════════════════════════
# WEBHOOK SERVER
# ═══════════════════════════════════════════════════════

class WhatsAppWebhookHandler(http.server.BaseHTTPRequestHandler):
    """Handle WhatsApp Cloud API webhooks."""

    def do_GET(self):
        """Webhook verification (Meta sends this during setup)."""
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        mode = params.get("hub.mode", [""])[0]
        token = params.get("hub.verify_token", [""])[0]
        challenge = params.get("hub.challenge", [""])[0]

        if mode == "subscribe" and token == WHATSAPP_VERIFY_TOKEN:
            print(f"  ✅ Webhook verified!")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(challenge.encode())
        else:
            print(f"  ❌ Webhook verification failed (token mismatch)")
            self.send_response(403)
            self.end_headers()

    def do_POST(self):
        """Receive incoming messages."""
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode()

        # Respond immediately (Meta requires 200 within 5 seconds)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

        # Process in background
        try:
            data = json.loads(body)
            entries = data.get("entry", [])
            for entry in entries:
                changes = entry.get("changes", [])
                for change in changes:
                    value = change.get("value", {})
                    messages = value.get("messages", [])
                    contacts = value.get("contacts", [])

                    for i, message in enumerate(messages):
                        contact = contacts[i] if i < len(contacts) else {}
                        threading.Thread(
                            target=process_whatsapp_message,
                            args=(message, contact),
                            daemon=True
                        ).start()
        except Exception as e:
            print(f"  ❌ Webhook error: {e}")

    def log_message(self, format, *args):
        pass


# ═══════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_ID:
        print("""
╔══════════════════════════════════════════════════════════╗
║     📱 Prime-AI WhatsApp Bot — Setup Required           ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  1. https://developers.facebook.com → Create App         ║
║  2. Add WhatsApp product                                 ║
║  3. Get test phone + token from dashboard                ║
║  4. Set webhook URL to:                                  ║
║     https://your-domain:3002/webhook                     ║
║  5. Subscribe to webhook field: "messages"               ║
║  6. Run:                                                 ║
║                                                          ║
║  $env:WHATSAPP_TOKEN = "your-token"                      ║
║  $env:WHATSAPP_PHONE_ID = "your-phone-number-id"         ║
║  python whatsapp_bot.py                                  ║
║                                                          ║
║  Or integrate with your existing OpenClaw WhatsApp!      ║
╚══════════════════════════════════════════════════════════╝
""")
        sys.exit(1)

    print(f"""
╔══════════════════════════════════════════════════════════╗
║     🇪🇺 Prime-AI WhatsApp Bot — RUNNING                 ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  Phone ID:  {WHATSAPP_PHONE_ID:<44}║
║  Webhook:   http://0.0.0.0:{PORT:<38}║
║  Verify:    {WHATSAPP_VERIFY_TOKEN:<44}║
║                                                          ║
║  Commands: /classify /scan /audit /roadmap /deadlines    ║
║  Free text → auto-classification                         ║
╚══════════════════════════════════════════════════════════╝
""")

    server = http.server.HTTPServer(("0.0.0.0", PORT), WhatsAppWebhookHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Bot stopped.")
        server.server_close()
