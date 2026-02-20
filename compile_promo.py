#!/usr/bin/env python3
"""
Prime-AI — Promo Video Compiler with Synth Music
==================================================
Generates a synthwave music track and compiles all 6 use case
videos into one premium promo video matching prime-ai.fr style.

Output: demo_videos/PRIME_AI_PROMO.mp4
"""
import os, struct, math, json, subprocess, sys
from pathlib import Path

os.environ.setdefault("HOME", os.environ.get("USERPROFILE", ""))

OUT = Path(__file__).parent / "demo_videos"
OUT.mkdir(exist_ok=True)

# ═══════════════════════════════════════════
#  STEP 1: Generate Synthwave Music Track
# ═══════════════════════════════════════════

def generate_music(filename, duration=90, sample_rate=44100):
    """Generate a professional synthwave/electronic music track."""
    print("  [music] Generating synthwave track...")

    samples = int(duration * sample_rate)
    data = []

    # Musical parameters
    bpm = 120
    beat = 60.0 / bpm  # seconds per beat
    bar = beat * 4      # seconds per bar

    # Chord progression (Am - F - C - G) in Hz
    chords = [
        [220.0, 261.6, 329.6],   # Am
        [174.6, 220.0, 261.6],   # F
        [261.6, 329.6, 392.0],   # C
        [196.0, 246.9, 293.7],   # G
    ]

    # Bass line notes
    bass_notes = [110.0, 87.3, 130.8, 98.0]

    # Arpeggio patterns
    arp_patterns = [
        [0, 1, 2, 1],
        [2, 1, 0, 1],
        [0, 2, 1, 2],
        [1, 0, 2, 0],
    ]

    for i in range(samples):
        t = i / sample_rate
        bar_pos = t / bar
        current_bar = int(bar_pos) % 4
        bar_frac = bar_pos - int(bar_pos)
        beat_pos = (t % beat) / beat

        chord = chords[current_bar]
        bass_note = bass_notes[current_bar]

        sample = 0.0

        # === KICK DRUM (4 on the floor) ===
        kick_t = t % beat
        if kick_t < 0.15:
            kick_freq = 150 * math.exp(-kick_t * 30)
            kick_env = math.exp(-kick_t * 15)
            sample += 0.35 * kick_env * math.sin(2 * math.pi * kick_freq * kick_t)

        # === HI-HAT (offbeat) ===
        hat_t = (t + beat/2) % beat
        if hat_t < 0.04:
            hat_env = math.exp(-hat_t * 80)
            # Noise approximation
            hat_noise = math.sin(t * 12345.6789) * math.sin(t * 7891.234)
            sample += 0.08 * hat_env * hat_noise

        # === SNARE (beats 2 and 4) ===
        snare_beat = int((t % (bar)) / beat)
        if snare_beat in (1, 3):
            snare_t = t % beat
            if snare_t < 0.1:
                snare_env = math.exp(-snare_t * 20)
                snare_tone = math.sin(2 * math.pi * 200 * snare_t)
                snare_noise = math.sin(t * 9876.5) * math.sin(t * 5432.1)
                sample += 0.15 * snare_env * (0.5 * snare_tone + 0.5 * snare_noise)

        # === BASS (sub + saw approximation) ===
        bass_env = 1.0 - 0.3 * beat_pos
        bass_phase = 2 * math.pi * bass_note * t
        bass_sub = math.sin(bass_phase)
        bass_saw = 0
        for h in range(1, 6):
            bass_saw += math.sin(h * bass_phase) / h * (-1 if h % 2 == 0 else 1)
        bass_saw *= 0.3
        sample += 0.2 * bass_env * (0.6 * bass_sub + 0.4 * bass_saw)

        # === PAD (lush chords with chorus) ===
        pad_vol = 0.08
        for note in chord:
            for detune in [-1.5, 0, 1.5]:  # Chorus effect
                freq = note * (2 ** (detune / 1200))
                phase = 2 * math.pi * freq * t
                pad_wave = math.sin(phase) + 0.5 * math.sin(2 * phase) + 0.25 * math.sin(3 * phase)
                sample += pad_vol * pad_wave / 3

        # === ARPEGGIO (16th notes) ===
        sixteenth = beat / 4
        arp_idx = int((t % bar) / sixteenth) % 4
        arp_pattern = arp_patterns[current_bar]
        arp_note_idx = arp_pattern[arp_idx]
        arp_freq = chord[arp_note_idx] * 2  # Octave up
        arp_t = t % sixteenth
        arp_env = math.exp(-arp_t * 12)
        arp_wave = math.sin(2 * math.pi * arp_freq * t)
        arp_wave += 0.5 * math.sin(4 * math.pi * arp_freq * t)

        # Intro/outro fade
        fade_in = min(1.0, t / 4.0)
        fade_out = min(1.0, (duration - t) / 3.0)
        master_vol = fade_in * fade_out

        # Section dynamics
        if t < 8:  # Intro: just bass + pad
            sample += 0.06 * arp_env * arp_wave * (t / 8)
        elif t < 16:  # Build
            sample += 0.08 * arp_env * arp_wave
        else:  # Full
            sample += 0.12 * arp_env * arp_wave

        # === LEAD MELODY (every 8 bars, simple melody) ===
        if t > 16:
            melody_bar = int(t / bar) % 8
            if melody_bar >= 4:
                melody_notes = [440, 523.3, 659.3, 523.3, 440, 392, 440, 523.3]
                melody_idx = int((t % (bar * 2)) / beat) % 8
                melody_freq = melody_notes[melody_idx]
                melody_t = t % beat
                melody_env = math.exp(-melody_t * 3) * 0.8
                lead = math.sin(2 * math.pi * melody_freq * t)
                lead += 0.7 * math.sin(4 * math.pi * melody_freq * t)
                lead += 0.3 * math.sin(6 * math.pi * melody_freq * t)
                sample += 0.07 * melody_env * lead

        sample *= master_vol * 0.5  # Master limiter
        sample = max(-0.95, min(0.95, sample))  # Clip protection
        data.append(sample)

    # Write WAV file
    wav_path = OUT / filename
    num_channels = 1
    bits_per_sample = 16
    byte_rate = sample_rate * num_channels * bits_per_sample // 8
    block_align = num_channels * bits_per_sample // 8
    data_size = len(data) * block_align

    with open(wav_path, 'wb') as f:
        # RIFF header
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + data_size))
        f.write(b'WAVE')
        # fmt chunk
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))
        f.write(struct.pack('<H', 1))  # PCM
        f.write(struct.pack('<H', num_channels))
        f.write(struct.pack('<I', sample_rate))
        f.write(struct.pack('<I', byte_rate))
        f.write(struct.pack('<H', block_align))
        f.write(struct.pack('<H', bits_per_sample))
        # data chunk
        f.write(b'data')
        f.write(struct.pack('<I', data_size))
        for s in data:
            f.write(struct.pack('<h', int(s * 32767)))

    size_mb = wav_path.stat().st_size / 1024 / 1024
    print(f"  [music] {wav_path.name} ({size_mb:.1f} MB, {duration}s)")
    return str(wav_path)


# ═══════════════════════════════════════════
#  STEP 2: Generate Title Cards (HTML → PNG)
# ═══════════════════════════════════════════

def create_title_card(text, subtitle, color, filename):
    """Create a title card HTML and screenshot it."""
    html = f"""<!DOCTYPE html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@800;900&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Inter',sans-serif;background:#05080f;color:#e8eaf6;
width:1280px;height:720px;display:flex;flex-direction:column;
align-items:center;justify-content:center;overflow:hidden}}
body::before{{content:'';position:absolute;top:0;left:0;right:0;bottom:0;
background:radial-gradient(ellipse at 40% 40%,{color}25 0%,transparent 50%),
radial-gradient(ellipse at 60% 60%,{color}15 0%,transparent 40%)}}
.content{{position:relative;z-index:1;text-align:center}}
.logo{{font-size:16px;letter-spacing:4px;color:{color};margin-bottom:24px;
text-transform:uppercase;font-weight:800}}
h1{{font-size:52px;font-weight:900;line-height:1.1;margin-bottom:16px;
background:linear-gradient(135deg,#fff 0%,{color} 100%);
-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
p{{font-size:20px;color:#7a82a6;max-width:600px}}
.bar{{position:absolute;bottom:40px;width:80%;height:3px;
background:linear-gradient(90deg,transparent,{color},{color},transparent);
border-radius:2px}}
</style></head><body>
<div class="content">
<div class="logo">▲ PRIME-AI</div>
<h1>{text}</h1>
<p>{subtitle}</p>
</div>
<div class="bar"></div>
</body></html>"""

    html_path = OUT / f"{filename}.html"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return str(html_path)


# ═══════════════════════════════════════════
#  STEP 3: Compile Final Video
# ═══════════════════════════════════════════

def find_ffmpeg():
    """Find ffmpeg from Playwright or system."""
    # Playwright bundles ffmpeg
    local = Path(os.environ.get("LOCALAPPDATA", ""))
    for ff in local.rglob("ffmpeg.exe"):
        return str(ff)
    return "ffmpeg"


def compile_promo(music_path):
    """Compile all videos + title cards + music into final promo."""
    print("\n  [compile] Building final promo video...")

    ff = find_ffmpeg()
    videos = []

    # Title cards to record
    cards = [
        ("intro", "EU AI Act\nCompliance System", "Scan · Classify · Audit · Report", "#6c63ff"),
        ("uc1_title", "Landing Page", "Premium marketing experience", "#00e676"),
        ("uc2_title", "Zero-Click Login", "Automatic JWT authentication", "#2196f3"),
        ("uc3_title", "AI Risk Classifier", "4 EU risk levels in seconds", "#ff9100"),
        ("uc4_title", "URL Scanner", "Scan any website for compliance", "#e91e63"),
        ("uc5_title", "9-Requirement Audit", "Articles 8-15 compliance check", "#9c27b0"),
        ("uc6_title", "Knowledge Base", "Complete regulatory database", "#00bcd4"),
        ("outro", "Prime-AI", "yace19ai.com · Yacine Benhamou", "#6c63ff"),
    ]

    # Generate title card HTMLs
    card_htmls = []
    for cid, title, sub, color in cards:
        html_path = create_title_card(title, sub, color, cid)
        card_htmls.append((cid, html_path))

    # Record title cards as short videos using Playwright
    from playwright.sync_api import sync_playwright

    print("  [compile] Recording title cards...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for cid, html_path in card_htmls:
            vid_dir = OUT / f"card_{cid}"
            vid_dir.mkdir(exist_ok=True)

            ctx = browser.new_context(
                viewport={"width": 1280, "height": 720},
                record_video_dir=str(vid_dir),
                record_video_size={"width": 1280, "height": 720},
            )
            page = ctx.new_page()
            page.goto(f"file:///{html_path.replace(os.sep, '/')}", wait_until="networkidle", timeout=5000)

            import time
            time.sleep(3)  # 3 second title card
            ctx.close()

            # Get the video
            vids = list(vid_dir.glob("*.webm"))
            if vids:
                dst = OUT / f"card_{cid}.webm"
                vids[0].rename(dst)
                videos.append(str(dst))
                print(f"    [card] {cid} OK")

        browser.close()

    # Build concat list: intro → [title → demo] × 6 → outro
    uc_videos = [
        ("uc1_title", "uc1_landing"),
        ("uc2_title", "uc2_auto_login"),
        ("uc3_title", "uc3_classifier"),
        ("uc4_title", "uc4_scanner"),
        ("uc5_title", "uc5_audit"),
        ("uc6_title", "uc6_kb"),
    ]

    # Create concat file
    concat_list = OUT / "concat.txt"
    with open(concat_list, 'w') as f:
        # Intro
        intro_path = OUT / "card_intro.webm"
        if intro_path.exists():
            f.write(f"file '{intro_path}'\n")

        for title_id, demo_id in uc_videos:
            card_path = OUT / f"card_{title_id}.webm"
            demo_path = OUT / f"{demo_id}.webm"
            if card_path.exists():
                f.write(f"file '{card_path}'\n")
            if demo_path.exists():
                f.write(f"file '{demo_path}'\n")

        # Outro
        outro_path = OUT / "card_outro.webm"
        if outro_path.exists():
            f.write(f"file '{outro_path}'\n")

    # Step 1: Concat all videos
    concat_output = OUT / "promo_no_audio.mp4"
    print("  [compile] Concatenating videos...")
    result = subprocess.run([
        ff, "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c:v", "libx264", "-preset", "fast",
        "-pix_fmt", "yuv420p", "-r", "30",
        "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=black",
        str(concat_output)
    ], capture_output=True, text=True, timeout=300)

    if result.returncode != 0:
        print(f"    [warn] concat error: {result.stderr[:200]}")
        return None

    # Step 2: Add music
    final_output = OUT / "PRIME_AI_PROMO.mp4"
    print("  [compile] Adding music...")

    # Get video duration
    probe = subprocess.run([
        ff, "-i", str(concat_output),
    ], capture_output=True, text=True)
    # Extract duration from stderr
    vid_duration = "90"
    for line in probe.stderr.split('\n'):
        if 'Duration' in line:
            parts = line.split('Duration:')[1].split(',')[0].strip()
            h, m, s = parts.split(':')
            vid_duration = str(int(float(h)*3600 + float(m)*60 + float(s)))
            break

    result2 = subprocess.run([
        ff, "-y",
        "-i", str(concat_output),
        "-i", str(music_path),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "128k",
        "-map", "0:v:0", "-map", "1:a:0",
        "-shortest",
        str(final_output)
    ], capture_output=True, text=True, timeout=300)

    if result2.returncode != 0:
        print(f"    [warn] audio merge: {result2.stderr[:200]}")
        # Fall back to video without audio
        concat_output.rename(final_output)

    if final_output.exists():
        size = final_output.stat().st_size / 1024 / 1024
        print(f"\n  [DONE] {final_output.name} ({size:.1f} MB)")
        return str(final_output)

    return None


def main():
    print("+" + "="*54 + "+")
    print("|  PRIME-AI — Promo Video Compiler                     |")
    print("|  Synthwave Music + 6 Use Cases → 1 Promo MP4         |")
    print("+" + "="*54 + "+")

    # Step 1: Generate music
    music = generate_music("synthwave_track.wav", duration=90)

    # Step 2: Compile final video
    result = compile_promo(music)

    if result:
        print(f"\n  {'='*54}")
        print(f"  PROMO VIDEO READY!")
        print(f"  {result}")
        print(f"  {'='*54}")
    else:
        print("\n  [!] Video compilation had issues but individual files are in demo_videos/")


if __name__ == "__main__":
    main()
