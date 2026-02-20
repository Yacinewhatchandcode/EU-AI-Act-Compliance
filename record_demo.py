#!/usr/bin/env python3
"""
Prime-AI — Full End-to-End Demo Video Recorder
================================================
Records 6 use case videos using Playwright's native video recording.
Each use case becomes a separate MP4 file ready for marketing.

Output: demo_videos/*.webm (auto-converted to .mp4 if ffmpeg available)
"""
import os, sys, time, json, subprocess
from pathlib import Path

os.environ.setdefault("HOME", os.environ.get("USERPROFILE", "C:\\Users\\Default"))

from playwright.sync_api import sync_playwright

BASE = "http://localhost:8080"
OUT = Path(__file__).parent / "demo_videos"
OUT.mkdir(exist_ok=True)

def smooth_scroll(page, target_y, steps=20, delay=0.04):
    """Smooth scroll animation."""
    current = page.evaluate("window.scrollY")
    step_size = (target_y - current) / steps
    for i in range(steps):
        page.evaluate(f"window.scrollTo(0, {int(current + step_size * (i+1))})")
        time.sleep(delay)

def smooth_type(page, selector, text, delay=0.05):
    """Type text with human-like speed."""
    page.click(selector)
    for char in text:
        page.keyboard.type(char)
        time.sleep(delay)

def record_use_case(browser, uc_id, title, actions_fn):
    """Record a single use case as video."""
    print(f"\n  {'='*50}")
    print(f"  Recording: {title}")
    print(f"  {'='*50}")

    vid_dir = OUT / f"raw_{uc_id}"
    vid_dir.mkdir(exist_ok=True)

    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        record_video_dir=str(vid_dir),
        record_video_size={"width": 1280, "height": 720},
        device_scale_factor=1,
    )

    page = context.new_page()

    # Pre-auth: get dev token
    try:
        page.goto(f"{BASE}/api/auth/dev", wait_until="networkidle", timeout=8000)
        auth_text = page.evaluate("document.body.innerText")
        auth = json.loads(auth_text)
        token = auth.get("token", "")
        user = json.dumps(auth.get("user", {})).replace("'", "\\'")
        page.goto(BASE, wait_until="domcontentloaded", timeout=8000)
        page.evaluate(f"localStorage.setItem('auth_token', '{token}')")
        page.evaluate(f"localStorage.setItem('auth_user', '{user}')")
        print(f"    [auth] JWT OK")
    except Exception as e:
        print(f"    [auth] skip: {e}")

    try:
        actions_fn(page)
    except Exception as e:
        print(f"    [error] {e}")

    # Get video path before closing
    video = page.video
    context.close()

    # Find the recorded video
    vids = list(vid_dir.glob("*.webm"))
    if vids:
        src = vids[0]
        dst = OUT / f"{uc_id}.webm"
        src.rename(dst)
        size = dst.stat().st_size / 1024 / 1024
        print(f"    [OK] {dst.name} ({size:.1f} MB)")

        # Convert to MP4
        mp4 = OUT / f"{uc_id}.mp4"
        try:
            ffmpeg_path = list(Path(os.environ.get("LOCALAPPDATA", "")) .rglob("ffmpeg.exe"))
            ff = str(ffmpeg_path[0]) if ffmpeg_path else "ffmpeg"
            subprocess.run([
                ff, "-y", "-i", str(dst),
                "-c:v", "libx264", "-preset", "fast",
                "-pix_fmt", "yuv420p", "-r", "30",
                str(mp4)
            ], capture_output=True, timeout=120)
            if mp4.exists():
                mp4_size = mp4.stat().st_size / 1024 / 1024
                print(f"    [OK] {mp4.name} ({mp4_size:.1f} MB)")
                return str(mp4)
        except Exception as e:
            print(f"    [warn] ffmpeg: {e}")
        return str(dst)
    else:
        print(f"    [warn] no video found")
        return None


# ═══════════════════════════════════════════
#  USE CASE ACTIONS
# ═══════════════════════════════════════════

def uc_landing(page):
    """UC1: Marketing landing page showcase."""
    page.goto(f"{BASE}/landing.html", wait_until="networkidle", timeout=15000)
    time.sleep(3)
    smooth_scroll(page, 400)
    time.sleep(2)
    smooth_scroll(page, 900)
    time.sleep(2)
    smooth_scroll(page, 1400)
    time.sleep(2)
    smooth_scroll(page, 2000)
    time.sleep(2)
    smooth_scroll(page, 2600)
    time.sleep(2)
    smooth_scroll(page, 3200)
    time.sleep(2)
    smooth_scroll(page, 0)
    time.sleep(2)

def uc_auto_login(page):
    """UC2: Zero-click auto login flow."""
    page.goto(f"{BASE}/login.html", wait_until="networkidle", timeout=15000)
    time.sleep(3)
    # The page should auto-login and redirect to main app
    time.sleep(5)
    # Show dashboard
    time.sleep(3)

def uc_classifier(page):
    """UC3: AI Risk Classifier - classify any AI system."""
    page.goto(BASE, wait_until="networkidle", timeout=15000)
    time.sleep(3)
    # Navigate to Classify screen
    try:
        page.click("[data-screen='classify']", timeout=3000)
    except:
        page.evaluate("typeof go === 'function' && go('classify')")
    time.sleep(1.5)
    # Type a description
    desc = "AI system that automatically screens job applicants CVs and makes hiring decisions based on personality traits and facial analysis"
    smooth_type(page, "#classifyInput", desc, 0.03)
    time.sleep(1)
    # Click classify
    page.click("#classifyBtn")
    time.sleep(6)
    # Scroll result
    try:
        page.evaluate("document.querySelector('.screen.active .screen-scroll')?.scrollBy({top: 300, behavior: 'smooth'})")
    except:
        pass
    time.sleep(3)

def uc_scanner(page):
    """UC4: URL Compliance Scanner."""
    page.goto(BASE, wait_until="networkidle", timeout=15000)
    time.sleep(2)
    try:
        page.click("[data-screen='scan']", timeout=3000)
    except:
        page.evaluate("typeof go === 'function' && go('scan')")
    time.sleep(1.5)
    smooth_type(page, "#scanUrl", "openai.com", 0.06)
    time.sleep(0.5)
    page.click("#scanBtn")
    time.sleep(8)
    try:
        page.evaluate("document.querySelector('.screen.active .screen-scroll')?.scrollBy({top: 400, behavior: 'smooth'})")
    except:
        pass
    time.sleep(3)

def uc_audit(page):
    """UC5: 9-Requirement Compliance Audit."""
    page.goto(BASE, wait_until="networkidle", timeout=15000)
    time.sleep(2)
    try:
        page.click("[data-screen='audit']", timeout=3000)
    except:
        page.evaluate("typeof go === 'function' && go('audit')")
    time.sleep(1.5)
    # Fill audit name
    try:
        smooth_type(page, "#auditName", "PrimeAI Recruitment System v2", 0.04)
    except:
        pass
    time.sleep(0.5)
    # Set slider values
    page.evaluate("""
        document.querySelectorAll('input[type=range]').forEach((s, i) => {
            s.value = [75, 60, 80, 50, 70, 85, 45, 90, 65][i] || 50;
            s.dispatchEvent(new Event('input'));
        })
    """)
    time.sleep(1)
    page.click("#auditBtn")
    time.sleep(6)
    try:
        page.evaluate("document.querySelector('.screen.active .screen-scroll')?.scrollBy({top: 400, behavior: 'smooth'})")
    except:
        pass
    time.sleep(3)

def uc_knowledge_base(page):
    """UC6: EU AI Act Knowledge Base browse."""
    page.goto(BASE, wait_until="networkidle", timeout=15000)
    time.sleep(2)
    try:
        page.click("[data-screen='kb']", timeout=3000)
    except:
        page.evaluate("typeof go === 'function' && go('kb')")
    time.sleep(2)
    try:
        scr = ".screen.active .screen-scroll"
        page.evaluate(f"document.querySelector('{scr}')?.scrollBy({{top: 300, behavior: 'smooth'}})")
        time.sleep(2)
        page.evaluate(f"document.querySelector('{scr}')?.scrollBy({{top: 300, behavior: 'smooth'}})")
        time.sleep(2)
        page.evaluate(f"document.querySelector('{scr}')?.scrollBy({{top: 300, behavior: 'smooth'}})")
        time.sleep(2)
        page.evaluate(f"document.querySelector('{scr}')?.scrollBy({{top: 300, behavior: 'smooth'}})")
        time.sleep(2)
    except:
        pass


# ═══════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════

USE_CASES = [
    ("uc1_landing",    "UC1: Marketing Landing Page",      uc_landing),
    ("uc2_auto_login", "UC2: Zero-Click Auto Login",       uc_auto_login),
    ("uc3_classifier", "UC3: AI Risk Classifier",          uc_classifier),
    ("uc4_scanner",    "UC4: URL Compliance Scanner",      uc_scanner),
    ("uc5_audit",      "UC5: 9-Requirement Audit",         uc_audit),
    ("uc6_kb",         "UC6: Knowledge Base",              uc_knowledge_base),
]

def main():
    print("+" + "="*54 + "+")
    print("|  Prime-AI — End-to-End Demo Recorder                 |")
    print("|  6 Use Cases → MP4 Videos for Marketing              |")
    print("+" + "="*54 + "+")

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for uc_id, title, action_fn in USE_CASES:
            path = record_use_case(browser, uc_id, title, action_fn)
            results.append({"id": uc_id, "title": title, "path": path})

        browser.close()

    # Summary
    print(f"\n\n  {'='*54}")
    print(f"  RESULTS")
    print(f"  {'='*54}")
    ok = 0
    for r in results:
        status = "[OK]" if r["path"] else "[FAIL]"
        if r["path"]:
            ok += 1
        print(f"  {status} {r['title']:<40s} {r['path'] or 'N/A'}")

    print(f"\n  {ok}/{len(results)} videos recorded")
    print(f"  Output: {OUT}")

    # Manifest
    with open(OUT / "manifest.json", "w") as f:
        json.dump({"videos": results, "total": len(results), "ok": ok}, f, indent=2)

    print(f"\n  Done!")

if __name__ == "__main__":
    main()
