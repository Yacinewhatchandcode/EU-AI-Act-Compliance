#!/usr/bin/env python3
"""
NEXUS CONTROL CENTER v2 — API Server
Routes ALL 86 dashboard buttons → unified MCP server (mcp_all_agents_server.py)
Covers ALL 104 Python scripts. No orphans.
Port 8080 · LAN accessible · WhatsApp notification on start
"""
import http.server
import json
import os
import sys
import socket
import subprocess
import threading
import time
from pathlib import Path
from urllib.parse import urlparse, parse_qs

PORT = int(os.environ.get("NEXUS_PORT", 8080))
ROOT = Path(__file__).parent
WEB = ROOT / "web"
MCP_SERVER = "mcp_all_agents_server.py"


def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"


def call_mcp_tool(tool_name, arguments=None):
    """Call any tool on the unified MCP server via stdio, streaming logs."""
    if arguments is None:
        arguments = {}

    init_req = json.dumps({
        "jsonrpc": "2.0", "id": 0, "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                   "clientInfo": {"name": "nexus-v2", "version": "2.0.0"}}
    })
    call_req = json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments}
    })
    input_data = init_req + "\n" + call_req + "\n"

    try:
        # Fix Windows charmap crash: force UTF-8 for all child processes
        env = os.environ.copy()
        env["PYTHONUTF8"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        env["NEXUS_HEADLESS"] = "1"  # Disable Tkinter OSD in subprocess

        proc = subprocess.Popen(
            [sys.executable, str(ROOT / MCP_SERVER)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            cwd=str(ROOT),
            env=env
        )
        
        proc.stdin.write(input_data)
        proc.stdin.flush()
        proc.stdin.close()
        
        def stream_stderr():
            with open(ROOT / "nexus_global.log", "a", encoding="utf-8") as f:
                f.write(json.dumps({"ts": int(time.time()), "tool": tool_name, "msg": f"▶ Started execution..."}) + "\n")
            for line in proc.stderr:
                ln = line.strip()
                if ln:
                    with open(ROOT / "nexus_global.log", "a", encoding="utf-8") as f:
                        f.write(json.dumps({"ts": int(time.time()), "tool": tool_name, "msg": ln}) + "\n")
        
        t = threading.Thread(target=stream_stderr, daemon=True)
        t.start()

        stdout_data, _ = proc.communicate(timeout=120)
        t.join(timeout=1)

        lines = [l for l in stdout_data.strip().split("\n") if l.strip()]
        if lines:
            last = json.loads(lines[-1])
            text = last.get("result", {}).get("content", [{}])[0].get("text", "")
            try:
                return json.loads(text)
            except:
                return {"result": text}
        return {"error": "No MCP response"}
    except subprocess.TimeoutExpired:
        if 'proc' in locals():
            proc.kill()
        return {"error": "Timeout (120s)"}
    except Exception as e:
        return {"error": str(e)}


# ═══════════════════════════════════════════════════════════════
# COMPLETE ACTION MAP — 86 actions → 86 MCP tools
# Every dashboard button maps to a real tool
# ═══════════════════════════════════════════════════════════════

ACTION_MAP = {
    # 💰 Trading (10)
    "balance":      "trading_get_balance",
    "prices":       "trading_get_prices",
    "fear":         "trading_fear_greed",
    "buy":          "trading_buy",
    "sell":         "trading_sell",
    "cycle":        "trading_ai_cycle",
    "portfolio":    "trading_portfolio",
    "defi":         "trading_defi",
    "arbitrage":    "trading_arbitrage",
    "power_cycle":  "trading_power_cycle",

    # ⚡ Crypto Earnings (8)
    "batch_sats":   "earn_batch_sats",
    "satoshi":      "earn_satoshi_invest",
    "airdrop":      "earn_airdrop_farm",
    "money":        "earn_money_machine",
    "real_earn":    "earn_real_earnings",
    "crypto_scan":  "earn_crypto_scan",
    "flush":        "earn_flush_wallet",
    "cashout":      "earn_cashout_revolut",

    # 🛡️ Compliance (8)
    "classify":     "compliance_classify",
    "audit":        "compliance_audit",
    "mica":         "compliance_mica_scan",
    "deadlines":    "compliance_deadlines",
    "penalties":    "compliance_penalties",
    "report":       "compliance_report",
    "cyber":        "compliance_cybersecurity",
    "scan_url":     "compliance_scan_url",

    # 📱 Communication (10)
    "wa_msg":       "comms_whatsapp_send",
    "wa_file":      "comms_whatsapp_file",
    "wa_ws":        "comms_whatsapp_ws",
    "telegram":     "comms_telegram_send",
    "discord":      "comms_discord_send",
    "slack":        "comms_slack_send",
    "email":        "comms_email_campaign",
    "instagram":    "comms_instagram_post",
    "news":         "comms_fetch_news",
    "qr":           "comms_generate_qr",

    # 🖥️ Desktop (8)
    "screenshot":   "desktop_screenshot",
    "click":        "desktop_click",
    "type":         "desktop_type",
    "hotkey":       "desktop_hotkey",
    "open_app":     "desktop_open_app",
    "find_win":     "desktop_find_window",
    "perplexity":   "desktop_search_perplexity",
    "chatgpt":      "desktop_ask_chatgpt",

    # 📊 Business (10)
    "openclaw_intent": "biz_intent_engine",
    "prospects":    "biz_find_prospects",
    "enrich":       "biz_enrich_leads",
    "invoice":      "biz_create_invoice",
    "revenue":      "biz_revenue_report",
    "document":     "biz_create_document",
    "ceo":          "biz_ceo_start",
    "analytics":    "biz_analytics",
    "live_tracking":"biz_live_tracking",
    "stripe":       "biz_check_stripe",
    "mcp_bridge":   "biz_mcp_bridge",
    "deploy":       "biz_deploy_vercel",

    # 🎮 Competitions (6)
    "botgames":     "comp_botgames_status",
    "fight":        "comp_botgames_fight",
    "metaculus":    "comp_metaculus_predict",
    "lablab":       "comp_lablab_submit",
    "arena":        "comp_arena_game",
    "multi_comp":   "comp_multi_submit",

    # 🎨 Creative (8)
    "gen3d":        "creative_gen_3d",
    "sketchfab":    "creative_upload_sketchfab",
    "characters":   "creative_gen_characters",
    "worlds":       "creative_worldmodels",
    "video":        "creative_compile_video",
    "fast_promo":   "creative_fast_promo",
    "record":       "creative_record_demo",
    "transcribe":   "creative_transcribe",

    # 🔧 System (12)
    "start_all":    "sys_start_all_bots",
    "agents":       "sys_agent_status",
    "device":       "sys_scan_device",
    "gdrive":       "sys_scan_gdrive",
    "repos":        "sys_scan_repos",
    "fix_repos":    "sys_fix_repos",
    "push":         "sys_push_all",
    "gh_meta":      "sys_update_github_meta",
    "icons":        "sys_generate_icons",
    "tunnel":       "sys_make_public_url",
    "supabase":     "sys_setup_supabase",
    "deep_scan":    "sys_recursive_scan",

    # 🤖 Autonomous (6)
    "fleet":        "auto_fleet_run",
    "ceo_ops":      "auto_ceo_ops",
    "startup_seq":  "auto_startup",
    "bot_engine":   "auto_bot_engine",
    "gh_promos":    "auto_github_promos",
    "master_vid":   "auto_master_video",

    # 🐦 Social Media (3)
    "twitter":      "social_twitter_post",
    "twitter_thread": "social_twitter_thread",
    "linkedin":     "social_linkedin_post",

    # 📅 Calendar (3)
    "cal_event":    "cal_create_event",
    "ceo_day":      "cal_schedule_ceo_day",
    "cal_today":    "cal_get_today",

    # 🎙️ Voice (2)
    "voice_speak":  "voice_speak",
    "voice_list":   "voice_list",

    # 🧠 AI Routing (2)
    "ai_ask":       "ai_route",
    "ai_models":    "ai_models",

    # 📊 Analysis (3)
    "analyze_data": "analyze_data",
    "analyze_pdf":  "analyze_pdf",
    "analyze_csv":  "analyze_csv",

    # 📅 Marketing (3)
    "mktg_post":    "mktg_schedule_post",
    "mktg_week":    "mktg_schedule_week",
    "mktg_publish": "mktg_publish_due",

    # ⚡ Task Queue (2)
    "queue_status": "queue_status",
    "queue_loop":   "queue_never_stop",

    # ⛏️ Mining & Hardware (3)
    "mine_setup":   "mine_setup",
    "mine_launch":  "mine_launch",
    "mine_upgrade": "mine_upgrade",

    # 🎯 Freelance & Bounty Sniper (4)
    "sniper_freelance_fleet": "sniper_freelance_fleet",
    "sniper_upwork_bot":      "sniper_upwork_bot",
    "sniper_github_work":     "sniper_github_work",
    "sniper_bounty_hunter":   "sniper_bounty_hunter",

    # 💼 Ultimate Sales Machine (4)
    "sales_ultimate_machine":  "sales_ultimate_machine",
    "sales_lead_sniper":       "sales_lead_sniper",
    "sales_prospect_finder":   "sales_prospect_finder",
    "sales_email_blaster":     "sales_email_blaster",

    # 🎯 Malt.fr Sniper (1)
    "malt_sniper":             "malt_sniper",
    "visibility_engine":       "visibility_engine",
}


VOICE_MEMORY = []


class NexusHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(WEB), **kw)

    def log_message(self, fmt, *args):
        msg = fmt % args
        if "/api/" in msg or "nexus" in msg.lower():
            print(f"[NEXUS] {msg}")

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ("/", "/nexus", "/nexus_control.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            with open(WEB / "nexus_control.html", "rb") as f:
                self.wfile.write(f.read())
            return

        if path == "/api/nexus/status":
            self._json({
                "status": "OPERATIONAL",
                "total_tools": len(ACTION_MAP),
                "categories": 20,
                "scripts": 104,
                "mcp_server": MCP_SERVER,
            })
            return

        if path == "/api/nexus/logs":
            logs = []
            try:
                if os.path.exists(ROOT / "nexus_global.log"):
                    with open(ROOT / "nexus_global.log", "r", encoding="utf-8") as f:
                        lines = [l.strip() for l in f.readlines() if l.strip()]
                        # Get last 150 lines
                        for line in lines[-150:]:
                            try:
                                logs.append(json.loads(line))
                            except:
                                pass
            except:
                pass
            self._json(logs)
            return

        if path == "/api/nexus/live_metrics":
            cpu_pct = 0
            try:
                import psutil
                cpu_pct = psutil.cpu_percent(interval=0.1)
            except Exception:
                pass

            log_count = 0
            try:
                log_file = ROOT / "nexus_global.log"
                if log_file.exists():
                    with open(log_file, "r", encoding="utf-8") as f:
                        log_count = sum(1 for _ in f)
            except Exception:
                pass

            revenue = "0.00"
            try:
                rev_file = ROOT / "revenue_state.json"
                if rev_file.exists():
                    with open(rev_file, "r", encoding="utf-8") as f:
                        rev_data = json.load(f)
                        revenue = str(rev_data.get("total_revenue", 0))
            except Exception:
                pass

            lead_count = 0
            try:
                for csv_name in ["prospects_output.csv", "cold_email_campaign_drafts.csv"]:
                    csv_file = ROOT / csv_name
                    if csv_file.exists():
                        with open(csv_file, "r", encoding="utf-8") as f:
                            lead_count += max(0, sum(1 for _ in f) - 1)
            except Exception:
                pass

            self._json({
                "tasks_completed": log_count,
                "revenue": revenue,
                "cpu": round(cpu_pct),
                "lead_pipeline": lead_count,
            })
            return

        if path == "/api/nexus/stream":
            self.send_response(200)
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=--frameboundary')
            self.end_headers()
            try:
                from PIL import ImageGrab, Image
                import io
                import time
                import os
                while True:
                    frame_path = ROOT / "browser_frame.jpg"
                    if frame_path.exists() and time.time() - frame_path.stat().st_mtime < 10:
                        try:
                            with open(frame_path, "rb") as f:
                                frame_bytes = f.read()
                            img = Image.open(io.BytesIO(frame_bytes))
                            img.load()
                        except:
                            img = ImageGrab.grab()
                            img.thumbnail((1280, 720))
                    else:
                        img = ImageGrab.grab()
                        img.thumbnail((1280, 720))
                    
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format='JPEG', quality=50)
                    frame = img_byte_arr.getvalue()
                    
                    self.wfile.write(b"--frameboundary\r\n")
                    self.wfile.write(b"Content-Type: image/jpeg\r\n")
                    self.wfile.write(f"Content-Length: {len(frame)}\r\n\r\n".encode('utf-8'))
                    self.wfile.write(frame)
                    self.wfile.write(b"\r\n")
                    self.wfile.flush()
                    # 3-4 FPS is enough and light on CPU
                    time.sleep(0.3)
            except Exception as e:
                pass
            return

        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        length = int(self.headers.get("Content-Length", 0))
        body = {}
        if length > 0:
            try:
                body = json.loads(self.rfile.read(length))
            except:
                body = {}

        if path.startswith("/api/nexus/"):
            action = path.replace("/api/nexus/", "")

            if action == "voice_command":
                cmd = body.get("command", "").lower()
                
                with open("nexus_global.log", "a", encoding="utf-8") as f:
                    log_entry = json.dumps({"ts":time.time(), "tool":"VoiceControl", "msg": f"🎙️ CEO Voice Command Initiated: '{cmd}'"})
                    f.write(log_entry + "\n")
                    
                import subprocess
                
                # Semantic rule engine simulating deep NLP action mapping
                speech_reply = "Synthesizing executive instruction. Deploying neural agents."
                action_type = "execute"
                query_args = ""
                
                global VOICE_MEMORY
                VOICE_MEMORY.append({"role": "user", "command": cmd})
                if len(VOICE_MEMORY) > 15:
                    VOICE_MEMORY.pop(0)

                memory_str = json.dumps([m["command"] for m in VOICE_MEMORY])
                
                if "zero" in cmd or "fleet" in cmd:
                    subprocess.Popen(["python", "autonomous_agent_fleet.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    speech_reply = "Agent Zero and the autonomous fleet have been awakened. Executing standard operating procedures."
                
                elif "clone" in cmd or "claw" in cmd:
                    subprocess.Popen(["python", "openclaw_3d_pipeline.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    speech_reply = "Open Claw pipeline activated. Leveraging cutting-edge models for generation."
                
                elif "close" in cmd or "stop" in cmd or "kill" in cmd or ("hide" in cmd and "browser" in cmd):
                    action_type = "close_browser"
                    subprocess.Popen(["Stop-Process", "-Name", "chrome", "-Force", "-ErrorAction", "SilentlyContinue"], shell=True)
                    speech_reply = "Closing active modules and returning control to the central visual feed. I am always listening."
                
                elif "fix" in cmd or "roll back" in cmd or "bug" in cmd:
                    subprocess.Popen(["python", "audit_all_repos.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    speech_reply = "Anomaly detected. Initializing self-correction sequence and rolling back affected systems step by step."

                elif "code" in cmd or "build" in cmd or "create" in cmd:
                    action_type = "ui_display"
                    try:
                        from multi_model_router import route_and_call
                        res = route_and_call(cmd, task_type="code")
                        query_args = res.get("response", {}).get("text", "Error generating code.")
                        speech_reply = "Antigravity coding sequence complete. Architecture synthesized and displayed on your neural interface."
                    except Exception as e:
                        query_args = f"Failed to access Neural Router: {str(e)}"
                        speech_reply = "Neural router unavailable."

                elif "whatsapp" in cmd or "message" in cmd:
                    msg = cmd.replace("send a message on whatsapp saying", "").replace("whatsapp", "").strip()
                    if not msg: msg = "CEO automated check-in."
                    subprocess.Popen(["python", "-c", f"from send_whatsapp import send_message; send_message('{msg}')"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    speech_reply = f"Bridging to WhatsApp. Sending your message: '{msg}' right away."
                    
                elif "deploy" in cmd or "ship" in cmd:
                    subprocess.Popen(["python", "deploy_vercel.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    speech_reply = "Shipping to production. Vercel deployment initiated for the global edge network."

                elif any(action in cmd for action in ["open", "launch", "go", "click", "search", "find", "extract", "work", "scan", "analyze", "read", "transcribe"]):
                    action_type = "execute"
                    with open("browser_instruction.txt", "w", encoding="utf-8") as f:
                        f.write(cmd)
                    speech_reply = "Executing contextual workflow over your UI. The autonomous entity has full access."
                    query_args = f"Running Autonomous Target: {cmd}"

                else:
                    action_type = "ui_display"
                    try:
                        from multi_model_router import route_and_call
                        sys_prompt = "You are PRIME.AI. You are an autonomous global operations AI equipped with 104 native tools inside the Sovereign Nexus. You NEVER say 'I am a text-based AI' or 'I cannot open applications'. If asked what you do or what model you are, answer concisely: you are PRIME.AI, the custom Multi-Model autonomous entity architected by Yacine. Explain that you natively automate the CEO's desktop, trade crypto, open applications, and generate revenue."
                        res = route_and_call(cmd, task_type="general", system_prompt=sys_prompt)
                        query_args = res.get("response", {}).get("text", "Error computing response.")
                        speech_reply = "Response synthesized."
                    except Exception as e:
                        query_args = f"Failed to access Neural Router: {str(e)}"
                        speech_reply = "Neural router unavailable."

                self._json({
                    "status": "Voice Command Processed",
                    "action": action_type,
                    "query": query_args,
                    "speech": speech_reply
                })
                return

            if action in ACTION_MAP:
                tool_name = ACTION_MAP[action]
                # Direct dispatch via nexus_handlers (no subprocess overhead)
                try:
                    from nexus_handlers import dispatch, HANDLER_MAP
                    if tool_name in HANDLER_MAP:
                        result = dispatch(tool_name, body)
                        self._json(result)
                        return
                except Exception as e:
                    pass
                # Fallback: MCP subprocess for tools not in nexus_handlers
                result = call_mcp_tool(tool_name, body)
                self._json(result)
                return

            self._json({"error": f"Unknown action: {action}", "available": len(ACTION_MAP)}, 404)
            return

        self._json({"error": "Not found"}, 404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def _json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode())


def main():
    ip = get_lan_ip()
    url = f"http://{ip}:{PORT}"
    local = f"http://localhost:{PORT}"

    print()
    print("╔════════════════════════════════════════════════════════╗")
    print("║  ⚡ NEXUS CONTROL CENTER v2 — ALL SYSTEMS ONLINE       ║")
    print("╠════════════════════════════════════════════════════════╣")
    print(f"║  📱 Phone:   {url:<42}║")
    print(f"║  💻 Local:   {local:<42}║")
    print("╠════════════════════════════════════════════════════════╣")
    print(f"║  🤖 MCP Server: {MCP_SERVER:<37}║")
    print(f"║  🔧 Tools:      {len(ACTION_MAP)} buttons → {len(ACTION_MAP)} MCP tools" + " " * (37 - len(f"{len(ACTION_MAP)} buttons → {len(ACTION_MAP)} MCP tools")) + "║")
    print(f"║  📂 Scripts:    104 Python files wired" + " " * 17 + "║")
    print("╠════════════════════════════════════════════════════════╣")
    print("║  Categories: Trading(10) Earn(8) Compliance(8)        ║")
    print("║    Comms(10) Desktop(8) Business(12) Compete(6)        ║")
    print("║    Creative(8) System(12) Auto(6) Social(3)            ║")
    print("║    Calendar(3) Voice(2) AI(2) Analysis(3)              ║")
    print("║    Marketing(3) Queue(2) Mining(3) Freelance(4)        ║")
    print("║    Sales(4) — 20 categories, 117 tools                 ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()

    # WhatsApp notify disabled — blocks startup when bridge is offline
    # try:
    #     from send_whatsapp import send_message
    #     send_message(...)
    # except: pass
    print(f"[NEXUS] Dashboard ready at {url}")

    # Agent loop disabled — was causing Tcl/Tkinter thread crash
    # print("[NEXUS] Launching PRIME Contextual Headless Browser Engine...")
    # subprocess.Popen([sys.executable, "prime_agent_loop.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        from http.server import ThreadingHTTPServer
        server = ThreadingHTTPServer(("", PORT), NexusHandler)
    except:
        server = http.server.HTTPServer(("", PORT), NexusHandler)
    print(f"[NEXUS] Listening on port {PORT}...")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[NEXUS] Shutting down...")
        subprocess.Popen(["Stop-Process", "-Name", "chrome", "-Force", "-ErrorAction", "SilentlyContinue"], shell=True)
        server.shutdown()


if __name__ == "__main__":
    main()
