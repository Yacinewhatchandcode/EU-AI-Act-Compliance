#!/usr/bin/env python3
"""
Prime-AI — Automated Demo Video Recorder
=========================================
Records browser-based demo videos for each use case.
Uses Playwright + ffmpeg to create polished MP4 promo videos.

Usage:
  pip install playwright
  playwright install chromium
  python record_demo.py

Output: demo_videos/ directory with MP4 files
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path

DEMO_DIR = Path(__file__).parent / "demo_videos"
DEMO_DIR.mkdir(exist_ok=True)

BASE_URL = "http://localhost:8080"

# ═══════════════════════════════════════════
#  USE CASES — Each becomes a demo video
# ═══════════════════════════════════════════

USE_CASES = [
    {
        "id": "01_landing",
        "title": "Prime-AI Landing Page",
        "description": "Marketing landing page with countdown, pricing, and feature showcase",
        "url": f"{BASE_URL}/landing.html",
        "actions": [
            {"type": "wait", "ms": 2000},
            {"type": "scroll", "y": 400, "ms": 1500},
            {"type": "scroll", "y": 900, "ms": 1500},
            {"type": "scroll", "y": 1400, "ms": 1500},
            {"type": "scroll", "y": 2000, "ms": 1500},
            {"type": "scroll", "y": 2600, "ms": 1500},
            {"type": "scroll", "y": 0, "ms": 2000},
        ]
    },
    {
        "id": "02_auto_login",
        "title": "Zero-Click Authentication",
        "description": "Auto JWT authentication — no manual login needed",
        "url": f"{BASE_URL}/",
        "actions": [
            {"type": "wait", "ms": 3000},
            {"type": "screenshot", "name": "dashboard"},
        ]
    },
    {
        "id": "03_url_scanner",
        "title": "URL Compliance Scanner",
        "description": "Scan any website for EU AI Act compliance",
        "url": f"{BASE_URL}/",
        "actions": [
            {"type": "wait", "ms": 2000},
            {"type": "click", "selector": "[data-screen='scan']"},
            {"type": "wait", "ms": 500},
            {"type": "type", "selector": "#scanUrl", "text": "openai.com"},
            {"type": "wait", "ms": 500},
            {"type": "click", "selector": "#scanBtn"},
            {"type": "wait", "ms": 8000},
            {"type": "scroll_el", "selector": ".screen-scroll", "y": 300, "ms": 1500},
            {"type": "screenshot", "name": "scan_result"},
        ]
    },
    {
        "id": "04_classifier",
        "title": "AI Risk Classifier",
        "description": "Classify any AI system into 4 EU risk levels",
        "url": f"{BASE_URL}/",
        "actions": [
            {"type": "wait", "ms": 2000},
            {"type": "click", "selector": "[data-screen='classify']"},
            {"type": "wait", "ms": 500},
            {"type": "type", "selector": "#classifyInput",
             "text": "AI system that screens job applicants' CVs and makes automated hiring decisions based on personality analysis"},
            {"type": "wait", "ms": 500},
            {"type": "click", "selector": "#classifyBtn"},
            {"type": "wait", "ms": 5000},
            {"type": "scroll_el", "selector": ".screen-scroll", "y": 200, "ms": 1000},
            {"type": "screenshot", "name": "classify_result"},
        ]
    },
    {
        "id": "05_audit",
        "title": "9-Requirement Compliance Audit",
        "description": "Full audit against Articles 8-15 of the EU AI Act",
        "url": f"{BASE_URL}/",
        "actions": [
            {"type": "wait", "ms": 2000},
            {"type": "click", "selector": "[data-screen='audit']"},
            {"type": "wait", "ms": 500},
            {"type": "type", "selector": "#auditName", "text": "PrimeAI Recruitment v2"},
            {"type": "wait", "ms": 300},
            # Set some slider values
            {"type": "eval", "code": "document.querySelectorAll('.audit-slider input[type=range]').forEach((s,i) => s.value = [75,60,80,50,70,85,45,90,65][i] || 50)"},
            {"type": "wait", "ms": 500},
            {"type": "click", "selector": "#auditBtn"},
            {"type": "wait", "ms": 5000},
            {"type": "scroll_el", "selector": ".screen-scroll", "y": 300, "ms": 1500},
            {"type": "screenshot", "name": "audit_result"},
        ]
    },
    {
        "id": "06_knowledge_base",
        "title": "EU AI Act Knowledge Base",
        "description": "Complete regulatory database — prohibited practices, high-risk categories, requirements",
        "url": f"{BASE_URL}/",
        "actions": [
            {"type": "wait", "ms": 2000},
            {"type": "click", "selector": "[data-screen='kb']"},
            {"type": "wait", "ms": 1000},
            {"type": "scroll_el", "selector": ".screen-scroll", "y": 400, "ms": 1500},
            {"type": "scroll_el", "selector": ".screen-scroll", "y": 800, "ms": 1500},
            {"type": "scroll_el", "selector": ".screen-scroll", "y": 1200, "ms": 1500},
            {"type": "screenshot", "name": "kb"},
        ]
    },
]


def record_use_case(page, uc):
    """Record a single use case as video frames."""
    print(f"\n{'='*60}")
    print(f"  Recording: {uc['title']}")
    print(f"  {uc['description']}")
    print(f"{'='*60}")

    uc_dir = DEMO_DIR / uc["id"]
    uc_dir.mkdir(exist_ok=True)

    # Navigate
    page.goto(uc["url"], wait_until="networkidle", timeout=15000)
    frame_n = 0

    for action in uc.get("actions", []):
        t = action["type"]

        if t == "wait":
            time.sleep(action["ms"] / 1000)
        elif t == "scroll":
            page.evaluate(f"window.scrollTo({{top: {action['y']}, behavior: 'smooth'}})")
            time.sleep(action.get("ms", 1000) / 1000)
        elif t == "scroll_el":
            page.evaluate(f"document.querySelector('{action['selector']}')?.scrollTo({{top: {action['y']}, behavior: 'smooth'}})")
            time.sleep(action.get("ms", 1000) / 1000)
        elif t == "click":
            try:
                page.click(action["selector"], timeout=3000)
            except Exception as e:
                print(f"  [warn] click failed: {e}")
            time.sleep(0.3)
        elif t == "type":
            try:
                page.fill(action["selector"], action["text"])
            except Exception as e:
                print(f"  [warn] type failed: {e}")
            time.sleep(0.3)
        elif t == "eval":
            try:
                page.evaluate(action["code"])
            except Exception as e:
                print(f"  [warn] eval failed: {e}")
        elif t == "screenshot":
            path = uc_dir / f"{action['name']}.png"
            page.screenshot(path=str(path), full_page=False)
            print(f"  [screenshot] {path}")

        # Capture frame after each action
        frame_path = uc_dir / f"frame_{frame_n:04d}.png"
        page.screenshot(path=str(frame_path), full_page=False)
        frame_n += 1
        print(f"  [frame {frame_n}] {t}")

    print(f"  => {frame_n} frames captured")
    return frame_n


def frames_to_video(uc_id, fps=2):
    """Convert frames to MP4 using ffmpeg."""
    uc_dir = DEMO_DIR / uc_id
    output = DEMO_DIR / f"{uc_id}.mp4"
    pattern = str(uc_dir / "frame_%04d.png")

    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", pattern,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=black",
        "-r", "30",
        str(output),
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            size_mb = output.stat().st_size / 1024 / 1024
            print(f"  [OK] {output.name} ({size_mb:.1f} MB)")
            return True
        else:
            print(f"  [WARN] ffmpeg failed: {result.stderr[:200]}")
            return False
    except FileNotFoundError:
        print("  [WARN] ffmpeg not found — frames saved as PNGs")
        return False
    except Exception as e:
        print(f"  [WARN] video conversion failed: {e}")
        return False


def main():
    print("╔══════════════════════════════════════════════╗")
    print("║  Prime-AI — Demo Video Recorder              ║")
    print("║  Recording all use cases for GitHub promo     ║")
    print("╚══════════════════════════════════════════════╝")

    # Try to import playwright
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("\n  Installing playwright...")
        subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            device_scale_factor=2,
        )

        # Start with video recording context
        page = context.new_page()

        # Auto-auth: get dev token
        print("\n  Getting dev JWT...")
        page.goto(f"{BASE_URL}/api/auth/dev", wait_until="networkidle")
        try:
            auth_json = page.evaluate("document.body.innerText")
            auth_data = json.loads(auth_json)
            token = auth_data.get("token", "")
            user = json.dumps(auth_data.get("user", {}))
            # Set in localStorage
            page.goto(BASE_URL, wait_until="domcontentloaded")
            page.evaluate(f"localStorage.setItem('auth_token', '{token}')")
            page.evaluate(f"localStorage.setItem('auth_user', '{user}')")
            print(f"  [OK] Authenticated as {auth_data.get('user', {}).get('email', '?')}")
        except Exception as e:
            print(f"  [WARN] Auth: {e}")

        # Record each use case
        total_frames = 0
        for uc in USE_CASES:
            frames = record_use_case(page, uc)
            total_frames += frames

        browser.close()

    # Convert frames to videos
    print("\n\n  Converting to MP4...")
    videos_ok = 0
    for uc in USE_CASES:
        if frames_to_video(uc["id"]):
            videos_ok += 1

    # Create master compilation script
    manifest = {
        "project": "Prime-AI EU AI Act Compliance",
        "website": "https://yace19ai.com",
        "github": "https://github.com/Yacinewhatchandcode",
        "use_cases": [
            {"id": uc["id"], "title": uc["title"], "description": uc["description"]}
            for uc in USE_CASES
        ],
        "total_frames": total_frames,
        "videos_created": videos_ok,
    }
    with open(DEMO_DIR / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\n{'='*60}")
    print(f"  DONE! {total_frames} frames, {videos_ok} videos")
    print(f"  Output: {DEMO_DIR}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
