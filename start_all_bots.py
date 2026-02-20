#!/usr/bin/env python3
"""
Prime-AI — Master Bot Launcher
================================
Starts all platform bots simultaneously.
One command to rule them all.

Usage:
  python start_all_bots.py
"""

import os
import sys
import subprocess
import time
from pathlib import Path

BOTS_DIR = Path(__file__).parent
BOTS = {
    "web": {
        "file": "eu_ai_act_server.py",
        "env_required": None,
        "icon": "🌐",
        "port": 8080,
    },
    "telegram": {
        "file": "telegram_bot.py",
        "env_required": "TELEGRAM_BOT_TOKEN",
        "icon": "📨",
        "port": None,
    },
    "slack": {
        "file": "slack_bot.py",
        "env_required": "SLACK_BOT_TOKEN",
        "icon": "💬",
        "port": 3001,
    },
    "whatsapp": {
        "file": "whatsapp_bot.py",
        "env_required": "WHATSAPP_TOKEN",
        "icon": "📱",
        "port": 3002,
    },
    "discord": {
        "file": "discord_bot.py",
        "env_required": "DISCORD_BOT_TOKEN",
        "icon": "🎮",
        "port": None,
    },
}


def check_env(var: str) -> bool:
    return bool(os.environ.get(var, ""))


def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║     🚀 Prime-AI — Multi-Platform Bot Launcher           ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║""")

    # Check which bots are configured
    ready = []
    not_ready = []

    for name, config in BOTS.items():
        env = config["env_required"]
        if env is None or check_env(env):
            ready.append(name)
            status = "✅ READY"
        else:
            not_ready.append(name)
            status = f"⚠️  Set ${env}"

        port_info = f" (:{config['port']})" if config['port'] else ""
        print(f"║  {config['icon']} {name.upper():<12} {status:<37}║")

    print("""║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")

    if not ready:
        print("❌ No bots configured! Set at least one token.")
        print("\nQuickest start:")
        print("  1. Get Telegram token from @BotFather")
        print("  2. $env:TELEGRAM_BOT_TOKEN = 'your-token'")
        print("  3. python start_all_bots.py")
        sys.exit(1)

    # Launch configured bots
    processes = []
    for name in ready:
        config = BOTS[name]
        filepath = BOTS_DIR / config["file"]
        if not filepath.exists():
            print(f"  ⚠️  {config['icon']} {name}: file not found ({filepath})")
            continue

        print(f"  {config['icon']} Starting {name}...")
        proc = subprocess.Popen(
            [sys.executable, str(filepath)],
            cwd=str(BOTS_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            text=True,
            env=os.environ.copy(),
        )
        processes.append((name, config, proc))
        time.sleep(1)

    if not_ready:
        print(f"\n  💡 {len(not_ready)} bot(s) not configured: {', '.join(not_ready)}")
        print("     Run individual bot files for setup instructions.\n")

    print(f"  🟢 {len(processes)} bot(s) running. Press Ctrl+C to stop all.\n")

    # Monitor output
    try:
        while True:
            for name, config, proc in processes:
                if proc.poll() is not None:
                    print(f"  ❌ {config['icon']} {name} exited with code {proc.returncode}")
                    # Read remaining output
                    output = proc.stdout.read()
                    if output:
                        for line in output.strip().split('\n')[-5:]:
                            print(f"     {line}")
                    processes.remove((name, config, proc))
                    break

            if not processes:
                print("\n  All bots stopped.")
                break

            time.sleep(2)

    except KeyboardInterrupt:
        print("\n\n  🛑 Stopping all bots...")
        for name, config, proc in processes:
            proc.terminate()
            print(f"     {config['icon']} {name} stopped")
        print("  Done.\n")


if __name__ == "__main__":
    main()
