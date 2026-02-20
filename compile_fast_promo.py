#!/usr/bin/env python3
"""
Prime-AI — 30s Fast Marketing Video
=====================================
Creates a fast-paced 15-30 second marketing clip:
- 2s intro title
- 2s per use case (6 × 2s = 12s) — speed-up of real demos
- 2s outro with CTA
- Synthwave beat underneath
- NO code visible, pure product showcase

Output: demo_videos/PRIME_AI_30s.mp4
"""
import os, struct, math, subprocess, time
from pathlib import Path

os.environ.setdefault("HOME", os.environ.get("USERPROFILE", ""))

from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent / "demo_videos"
OUT.mkdir(exist_ok=True)


def find_ffmpeg():
    local = Path(os.environ.get("LOCALAPPDATA", ""))
    for ff in local.rglob("ffmpeg.exe"):
        return str(ff)
    return "ffmpeg"


def generate_fast_beat(filename, duration=30, sr=44100):
    """Generate a fast energetic beat for 30s clip."""
    print("  [beat] Generating 30s beat...")
    samples = int(duration * sr)
    data = []
    bpm = 140  # Faster tempo
    beat = 60.0 / bpm

    bass_notes = [110, 87.3, 130.8, 98]
    chords = [[220, 261.6, 329.6], [174.6, 220, 261.6],
              [261.6, 329.6, 392], [196, 246.9, 293.7]]

    for i in range(samples):
        t = i / sr
        bar = beat * 4
        cb = int((t / bar)) % 4
        s = 0.0

        # Kick
        kt = t % beat
        if kt < 0.12:
            kf = 160 * math.exp(-kt * 35)
            s += 0.4 * math.exp(-kt * 18) * math.sin(2 * math.pi * kf * kt)

        # Hihat
        ht = (t + beat/2) % (beat/2)
        if ht < 0.02:
            s += 0.06 * math.exp(-ht * 100) * math.sin(t * 15000) * math.sin(t * 8000)

        # Bass
        bf = bass_notes[cb]
        bp = 2 * math.pi * bf * t
        s += 0.15 * math.sin(bp) + 0.05 * math.sin(2 * bp)

        # Pad
        for n in chords[cb]:
            s += 0.04 * math.sin(2 * math.pi * n * t)

        # Arp (fast 16th notes)
        sixteenth = beat / 4
        ai = int((t % bar) / sixteenth) % 3
        af = chords[cb][ai] * 2
        at = t % sixteenth
        s += 0.08 * math.exp(-at * 15) * math.sin(2 * math.pi * af * t)

        # Risers (every 8 seconds)
        riser_pos = t % 8
        if riser_pos > 6:
            rf = 200 + (riser_pos - 6) * 2000
            s += 0.03 * math.sin(2 * math.pi * rf * t)

        # Fades
        fade = min(1, t / 1.5) * min(1, (duration - t) / 1.5)
        s *= fade * 0.5
        s = max(-0.95, min(0.95, s))
        data.append(s)

    path = OUT / filename
    with open(path, 'wb') as f:
        f.write(b'RIFF')
        ds = len(data) * 2
        f.write(struct.pack('<I', 36 + ds))
        f.write(b'WAVE')
        f.write(b'fmt ')
        f.write(struct.pack('<IHHIIHH', 16, 1, 1, sr, sr * 2, 2, 16))
        f.write(b'data')
        f.write(struct.pack('<I', ds))
        for v in data:
            f.write(struct.pack('<h', int(v * 32767)))

    print(f"  [beat] {path.name} ({path.stat().st_size/1024:.0f} KB)")
    return str(path)


def create_slide(text, subtitle, color, accent, idx):
    """Create a premium marketing slide."""
    html = f"""<!DOCTYPE html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Inter',sans-serif;background:#05080f;color:#fff;
width:1280px;height:720px;display:flex;align-items:center;justify-content:center;overflow:hidden}}
body::before{{content:'';position:absolute;inset:0;
background:radial-gradient(ellipse at 30% 40%,{color}30 0%,transparent 50%),
radial-gradient(ellipse at 70% 70%,{accent}20 0%,transparent 40%)}}
.c{{position:relative;z-index:1;text-align:center;padding:40px}}
.logo{{font-size:13px;letter-spacing:5px;color:{color};margin-bottom:20px;
font-weight:700;text-transform:uppercase}}
.logo::before{{content:'▲ '}}
h1{{font-size:48px;font-weight:900;line-height:1.1;margin-bottom:14px;
background:linear-gradient(135deg,#fff 30%,{color});
-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
p{{font-size:18px;color:#8892b0;max-width:500px;margin:0 auto}}
.num{{position:absolute;top:30px;right:40px;font-size:72px;font-weight:900;
color:{color}12;letter-spacing:-3px}}
.bar{{position:absolute;bottom:0;left:0;right:0;height:3px;
background:linear-gradient(90deg,transparent,{color},{accent},transparent)}}
.cta{{display:inline-block;margin-top:20px;padding:12px 32px;background:{color};
color:#fff;font-weight:700;border-radius:8px;font-size:16px}}
</style></head><body>
<div class="c">
<div class="logo">PRIME-AI</div>
<h1>{text}</h1>
<p>{subtitle}</p>
{f'<div class="cta">Start Free →</div>' if idx == 99 else ''}
</div>
<div class="num">{f"0{idx}" if idx < 10 and idx > 0 else ""}</div>
<div class="bar"></div>
</body></html>"""
    path = OUT / f"fast_{idx:02d}.html"
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return str(path)


def main():
    print("+" + "="*50 + "+")
    print("|  PRIME-AI — 30s Fast Marketing Video            |")
    print("|  For yace19ai.com + GitHub                      |")
    print("+" + "="*50 + "+")

    ff = find_ffmpeg()

    # 1. Generate beat
    beat_path = generate_fast_beat("fast_beat.wav", duration=30)

    # 2. Create slides
    slides = [
        (0, "EU AI Act\nCompliance", "Scan · Classify · Audit · Report", "#6c63ff", "#00e676"),
        (1, "URL Scanner", "Scan any website in seconds", "#00e676", "#2196f3"),
        (2, "Risk Classifier", "4 EU risk levels — instant", "#ff9100", "#e91e63"),
        (3, "Compliance Audit", "9 requirements · Articles 8-15", "#9c27b0", "#6c63ff"),
        (4, "Knowledge Base", "Complete regulatory database", "#00bcd4", "#00e676"),
        (5, "Multi-Platform", "Web · Telegram · Slack · Discord", "#2196f3", "#ff9100"),
        (6, "Zero Setup", "Auto-login · No config needed", "#00e676", "#6c63ff"),
        (99, "Start Free Today", "prime-ai.fr · yace19ai.com", "#6c63ff", "#00e676"),
    ]

    for idx, text, sub, color, accent in slides:
        create_slide(text, sub, color, accent, idx)

    # 3. Record slides (2s each) + speed-up demo clips
    print("\n  [record] Recording fast clips...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        clip_paths = []

        for idx, text, sub, color, accent in slides:
            vid_dir = OUT / f"fast_card_{idx:02d}"
            vid_dir.mkdir(exist_ok=True)

            ctx = browser.new_context(
                viewport={"width": 1280, "height": 720},
                record_video_dir=str(vid_dir),
                record_video_size={"width": 1280, "height": 720},
            )
            page = ctx.new_page()
            html_path = OUT / f"fast_{idx:02d}.html"
            page.goto(f"file:///{str(html_path).replace(os.sep, '/')}")
            time.sleep(2.5 if idx in (0, 99) else 2)
            ctx.close()

            vids = list(vid_dir.glob("*.webm"))
            if vids:
                dst = OUT / f"fast_clip_{idx:02d}.webm"
                vids[0].rename(dst)
                clip_paths.append(str(dst))
                print(f"    [clip] slide {idx:02d} OK")

        browser.close()

    # 4. Speed up real demo clips (take 3s from middle, 4x speed)
    print("\n  [speedup] Creating fast demo inserts...")
    demo_files = ["uc1_landing", "uc3_classifier", "uc4_scanner", "uc5_audit"]
    fast_demos = []

    for demo_id in demo_files:
        src = OUT / f"{demo_id}.webm"
        if not src.exists():
            continue
        dst = OUT / f"fast_demo_{demo_id}.webm"
        # Take middle 8 seconds, speed up 4x → 2 seconds
        result = subprocess.run([
            ff, "-y", "-ss", "3", "-t", "8", "-i", str(src),
            "-vf", "setpts=0.25*PTS,scale=1280:720",
            "-an", "-r", "30",
            str(dst)
        ], capture_output=True, text=True, timeout=60)
        if dst.exists():
            fast_demos.append(str(dst))
            print(f"    [fast] {demo_id} → 2s OK")

    # 5. Build concat list (alternating titles and fast demos)
    concat_file = OUT / "fast_concat.txt"
    with open(concat_file, 'w') as f:
        # Intro (slide 0)
        f.write(f"file '{clip_paths[0]}'\n")

        # For each feature, interleave title + fast demo if available
        for i, clip in enumerate(clip_paths[1:-1], 0):
            f.write(f"file '{clip}'\n")
            if i < len(fast_demos):
                f.write(f"file '{fast_demos[i]}'\n")

        # Outro
        f.write(f"file '{clip_paths[-1]}'\n")

    # 6. Concat
    print("\n  [compile] Concatenating...")
    no_audio = OUT / "fast_no_audio.mp4"
    subprocess.run([
        ff, "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c:v", "libx264", "-preset", "fast",
        "-pix_fmt", "yuv420p", "-r", "30",
        "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=black",
        "-t", "30",
        str(no_audio)
    ], capture_output=True, timeout=120)

    # 7. Add beat
    print("  [compile] Adding beat...")
    final = OUT / "PRIME_AI_30s.mp4"
    subprocess.run([
        ff, "-y",
        "-i", str(no_audio),
        "-i", beat_path,
        "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
        "-map", "0:v:0", "-map", "1:a:0",
        "-shortest",
        str(final)
    ], capture_output=True, timeout=120)

    if final.exists():
        size = final.stat().st_size / 1024 / 1024
        print(f"\n  {'='*50}")
        print(f"  DONE! PRIME_AI_30s.mp4 ({size:.1f} MB)")
        print(f"  {final}")
        print(f"  {'='*50}")
    else:
        print("  [!] Final compilation failed, check individual clips")


if __name__ == "__main__":
    main()
