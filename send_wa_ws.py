"""
Send files via OpenClaw WhatsApp Gateway (WebSocket protocol)
"""
import websocket
import json
import time
import base64
import os
import sys
import mimetypes

GATEWAY_WS = "ws://127.0.0.1:18789/ws"
TOKEN = "c986696dc5cdf9bc04fa290f8a227a7083dbe57162981b78"
PHONE = "+33762679434"


def send_via_ws(message, media_path=None):
    """Send message (and optionally a file) via the OpenClaw WebSocket gateway."""
    
    ws = websocket.create_connection(GATEWAY_WS, timeout=15)
    
    # Step 1: Connect with auth
    connect_msg = json.dumps({
        "type": "connect",
        "token": TOKEN,
        "role": "operator",
    })
    ws.send(connect_msg)
    
    # Wait for hello-ok
    for _ in range(5):
        resp = ws.recv()
        data = json.loads(resp)
        print(f"  <- {data.get('type', 'unknown')}")
        if data.get("type") == "hello-ok" or data.get("status") == "ok":
            break
    
    # Step 2: Build the send request
    params = {
        "channel": "whatsapp",
        "to": PHONE,
        "text": message,
    }
    
    if media_path and os.path.exists(media_path):
        filename = os.path.basename(media_path)
        mime, _ = mimetypes.guess_type(media_path)
        if not mime:
            mime = "application/octet-stream"
        
        with open(media_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        
        params["media"] = {
            "data": f"data:{mime};base64,{b64}",
            "mimetype": mime,
            "filename": filename,
        }
        print(f"  📎 Attaching: {filename} ({mime})")
    
    send_msg = json.dumps({
        "type": "req",
        "method": "channels.send",
        "id": "send-1",
        "params": params,
    })
    
    ws.send(send_msg)
    print(f"  -> Sent message request")
    
    # Wait for response
    for _ in range(10):
        try:
            resp = ws.recv()
            data = json.loads(resp)
            msg_type = data.get("type", "")
            print(f"  <- {msg_type}: {json.dumps(data)[:200]}")
            
            if msg_type == "res" or data.get("status") in ("ok", "error"):
                break
        except websocket.WebSocketTimeoutException:
            break
    
    ws.close()
    print("  ✅ Done")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python send_wa_ws.py 'message text'")
        print("  python send_wa_ws.py 'caption' path/to/file")
        sys.exit(0)
    
    message = sys.argv[1]
    media = sys.argv[2] if len(sys.argv) > 2 else None
    
    send_via_ws(message, media)
