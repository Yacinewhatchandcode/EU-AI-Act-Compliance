"""
Send files via OpenClaw WhatsApp Gateway
"""
import requests
import sys
import os
import json
import base64

GATEWAY_URL = "http://127.0.0.1:18789"
GATEWAY_TOKEN = "c986696dc5cdf9bc04fa290f8a227a7083dbe57162981b78"
PHONE = "+33762679434"

HEADERS = {
    "Authorization": f"Bearer {GATEWAY_TOKEN}",
    "Content-Type": "application/json",
}


def send_message(text):
    """Send a text message via WhatsApp."""
    payload = {
        "jsonrpc": "2.0",
        "method": "sendMessage",
        "id": 1,
        "params": {
            "channel": "whatsapp",
            "to": PHONE,
            "text": text,
        }
    }
    try:
        r = requests.post(f"{GATEWAY_URL}/rpc", json=payload, headers=HEADERS, timeout=15)
        print(f"Message sent: {r.status_code} - {r.text[:200]}")
        return r.json()
    except Exception as e:
        print(f"Error: {e}")
        return None


def send_file(file_path, caption=""):
    """Send a file via WhatsApp."""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    
    filename = os.path.basename(file_path)
    
    # Read file and encode as base64
    with open(file_path, "rb") as f:
        file_data = base64.b64encode(f.read()).decode('utf-8')
    
    # Determine mime type
    ext = os.path.splitext(filename)[1].lower()
    mime_types = {
        '.csv': 'text/csv',
        '.html': 'text/html',
        '.pdf': 'application/pdf',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    }
    mime = mime_types.get(ext, 'application/octet-stream')
    
    payload = {
        "jsonrpc": "2.0",
        "method": "sendMessage",
        "id": 1,
        "params": {
            "channel": "whatsapp",
            "to": PHONE,
            "text": caption or filename,
            "media": {
                "data": file_data,
                "mimetype": mime,
                "filename": filename,
            }
        }
    }
    
    try:
        r = requests.post(f"{GATEWAY_URL}/rpc", json=payload, headers=HEADERS, timeout=30)
        print(f"File sent ({filename}): {r.status_code} - {r.text[:200]}")
        return r.json()
    except Exception as e:
        print(f"Error sending file: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python send_whatsapp.py message 'Hello!'")
        print("  python send_whatsapp.py file path/to/file.pdf 'Caption'")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "message":
        text = sys.argv[2] if len(sys.argv) > 2 else "Test from PRIME.AI"
        send_message(text)
    
    elif cmd == "file":
        path = sys.argv[2] if len(sys.argv) > 2 else ""
        caption = sys.argv[3] if len(sys.argv) > 3 else ""
        send_file(path, caption)
    
    else:
        print(f"Unknown: {cmd}")
