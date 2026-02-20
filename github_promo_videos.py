#!/usr/bin/env python3
"""
Prime-AI — GitHub Repos Promo Video Generator
===============================================
Creates professional promo videos for each GitHub repo.
For repos with live URLs, records browser demos.
For others, generates animated text-based showcase videos.

Usage:
  python github_promo_videos.py

Output: promo_videos/ directory
"""

import json
import os
import subprocess
import sys
from pathlib import Path

PROMO_DIR = Path(__file__).parent / "promo_videos"
PROMO_DIR.mkdir(exist_ok=True)

# ═══════════════════════════════════════════
#  ALL GITHUB REPOS — @Yacinewhatchandcode
# ═══════════════════════════════════════════

REPOS = [
    {
        "name": "Yace19ai.com",
        "desc": "Professional portfolio showcasing AI Builder expertise with ASIREM multi-agent ecosystem",
        "url": "https://yace19ai.com",
        "tech": ["React", "Three.js", "Framer Motion", "Netlify"],
        "color": "#0891b2",
        "category": "Portfolio",
    },
    {
        "name": "EU-AI-Act-Compliance",
        "desc": "Full-stack EU AI Act compliance toolkit — scanner, classifier, auditor, multi-platform bots",
        "url": "http://localhost:8080",
        "tech": ["Python", "PWA", "JWT", "Material Design 3"],
        "color": "#6c63ff",
        "category": "RegTech",
    },
    {
        "name": "Sovereign-Ecosystem",
        "desc": "The complete Sovereign Ecosystem codebase including aSiReM agents, dashboard, and infrastructure",
        "url": None,
        "tech": ["Multi-Agent", "Infrastructure", "Dashboard"],
        "color": "#00e676",
        "category": "AI Infrastructure",
    },
    {
        "name": "AgentY",
        "desc": "Multi-Agent AI Coding System",
        "url": None,
        "tech": ["AI Agents", "Code Generation", "Multi-Agent"],
        "color": "#ff9100",
        "category": "AI Agents",
    },
    {
        "name": "ran-sales-copilot",
        "desc": "AI-powered sales copilot for automated prospecting and outreach",
        "url": None,
        "tech": ["Sales AI", "CRM", "Automation"],
        "color": "#e91e63",
        "category": "Sales AI",
    },
    {
        "name": "Mesekai",
        "desc": "Personal webcam motion tracking avatar",
        "url": None,
        "tech": ["Computer Vision", "Motion Tracking", "WebCam"],
        "color": "#9c27b0",
        "category": "Computer Vision",
    },
    {
        "name": "antigravity-game",
        "desc": "Antigravity: Space Explorer — 3D platformer with gravity flip mechanics + JEPA AI Agent",
        "url": None,
        "tech": ["Three.js", "Vite", "3D", "JEPA"],
        "color": "#2196f3",
        "category": "Game Dev",
    },
    {
        "name": "PrimeCrypto",
        "desc": "AI-Powered Crypto Platform on Base blockchain",
        "url": None,
        "tech": ["Crypto", "Base", "AI Trading", "DeFi"],
        "color": "#ffd700",
        "category": "Crypto",
    },
    {
        "name": "VoiceCloning",
        "desc": "F5-TTS Voice Cloning & Training System",
        "url": None,
        "tech": ["TTS", "Voice Cloning", "F5-TTS", "ML"],
        "color": "#ff5252",
        "category": "Voice AI",
    },
    {
        "name": "calendly-connect",
        "desc": "Calendly integration for automated scheduling",
        "url": None,
        "tech": ["Calendly", "API", "Scheduling"],
        "color": "#006bff",
        "category": "Integration",
    },
    {
        "name": "NETWORKING",
        "desc": "Prime AI NETWORKING — Dashboard, Cyber Radar, Games",
        "url": None,
        "tech": ["Dashboard", "Cyber", "Networking"],
        "color": "#00bfa5",
        "category": "Security",
    },
    {
        "name": "mcp-registry",
        "desc": "Docker MCP registry fork",
        "url": None,
        "tech": ["Docker", "MCP", "Registry"],
        "color": "#2496ed",
        "category": "Infrastructure",
    },
    {
        "name": "Faith",
        "desc": "VideoGenerator — AI video creation tool",
        "url": None,
        "tech": ["Video", "AI", "Generation"],
        "color": "#7c4dff",
        "category": "Content AI",
    },
    {
        "name": "AIA-Creative-Lab",
        "desc": "Vision 2030 — Creative AI laboratory",
        "url": None,
        "tech": ["Creative AI", "Vision", "Lab"],
        "color": "#ff6d00",
        "category": "Creative AI",
    },
    {
        "name": "AIA-DiscoVery",
        "desc": "AI-powered discovery platform",
        "url": None,
        "tech": ["Discovery", "AI", "Platform"],
        "color": "#00c853",
        "category": "AI Platform",
    },
    {
        "name": "hyperswitch-cloud",
        "desc": "Hyperswitch cloud payment orchestration",
        "url": None,
        "tech": ["Payments", "Orchestration", "Cloud"],
        "color": "#536dfe",
        "category": "FinTech",
    },
    {
        "name": "converse-final-solution",
        "desc": "AI conversation platform",
        "url": None,
        "tech": ["Conversational AI", "NLP", "Chat"],
        "color": "#e040fb",
        "category": "Conversational AI",
    },
    {
        "name": "BSQ",
        "desc": "Algorithm project — Board Square optimization",
        "url": None,
        "tech": ["Algorithms", "C", "Optimization"],
        "color": "#455a64",
        "category": "Algorithms",
    },
    {
        "name": "SQ_BAHA",
        "desc": "Algorithm project — Square Baha",
        "url": None,
        "tech": ["Algorithms", "C"],
        "color": "#546e7a",
        "category": "Algorithms",
    },
    {
        "name": "AgentCoderYBE",
        "desc": "AI coding agent — autonomous code generation",
        "url": None,
        "tech": ["AI Agent", "Code Gen", "Autonomous"],
        "color": "#ff3d00",
        "category": "AI Agents",
    },
    {
        "name": "lovable-spirit-forge",
        "desc": "Spirit Forge — lovable AI creation platform",
        "url": None,
        "tech": ["AI", "Creative", "Platform"],
        "color": "#d500f9",
        "category": "Creative AI",
    },
]


def generate_html_slide(repo, output_path):
    """Generate an HTML slide for a repo that can be screenshotted."""
    tech_badges = "".join(
        f'<span class="badge">{t}</span>' for t in repo["tech"]
    )

    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap" rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
    font-family: 'Inter', sans-serif;
    background: #05080f;
    color: #e8eaf6;
    width: 1280px; height: 720px;
    display: flex; align-items: center; justify-content: center;
    overflow: hidden;
}}
.slide {{
    width: 100%; height: 100%; padding: 80px;
    display: flex; flex-direction: column; justify-content: center;
    position: relative;
}}
.slide::before {{
    content: '';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at 30% 40%, {repo['color']}22 0%, transparent 60%),
                radial-gradient(ellipse at 70% 60%, {repo['color']}11 0%, transparent 50%);
}}
.content {{ position: relative; z-index: 1; }}
.category {{
    font-size: 14px; font-weight: 600; color: {repo['color']};
    text-transform: uppercase; letter-spacing: 2px; margin-bottom: 16px;
}}
h1 {{
    font-size: 56px; font-weight: 900; letter-spacing: -1px;
    margin-bottom: 20px; line-height: 1.1;
}}
h1 span {{ color: {repo['color']}; }}
.desc {{
    font-size: 22px; color: #9fa8c4; line-height: 1.6;
    max-width: 700px; margin-bottom: 32px;
}}
.badges {{ display: flex; gap: 10px; flex-wrap: wrap; }}
.badge {{
    background: {repo['color']}22;
    border: 1px solid {repo['color']}44;
    color: {repo['color']};
    padding: 6px 16px; border-radius: 20px;
    font-size: 14px; font-weight: 600;
}}
.author {{
    position: absolute; bottom: 40px; right: 60px;
    font-size: 14px; color: #4a5578;
}}
.author strong {{ color: #9fa8c4; }}
.github-icon {{
    position: absolute; top: 40px; right: 60px;
    font-size: 14px; color: #4a5578;
}}
</style></head>
<body>
<div class="slide">
    <div class="content">
        <div class="category">{repo['category']}</div>
        <h1><span>{repo['name']}</span></h1>
        <p class="desc">{repo['desc']}</p>
        <div class="badges">{tech_badges}</div>
    </div>
    <div class="github-icon">github.com/Yacinewhatchandcode/{repo['name']}</div>
    <div class="author"><strong>Yacine Benhamou</strong> | yace19ai.com</div>
</div>
</body></html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path


def create_overview_html(repos, output_path):
    """Create the final overview slide showing all repos."""
    cards = ""
    for r in repos[:15]:
        cards += f"""
        <div class="repo-card" style="border-color: {r['color']}44">
            <span class="dot" style="background:{r['color']}"></span>
            <span class="rname">{r['name']}</span>
            <span class="rcat">{r['category']}</span>
        </div>"""

    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap" rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
    font-family: 'Inter', sans-serif;
    background: #05080f; color: #e8eaf6;
    width: 1280px; height: 720px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 40px;
}}
h1 {{ font-size: 36px; font-weight: 900; margin-bottom: 12px; }}
h1 span {{ color: #6c63ff; }}
.sub {{ color: #4a5578; font-size: 16px; margin-bottom: 32px; }}
.grid {{
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 12px; width: 100%;
}}
.repo-card {{
    background: #0c1120;
    border: 1px solid #1c2236;
    padding: 14px 18px; border-radius: 10px;
    display: flex; align-items: center; gap: 10px;
    font-size: 14px;
}}
.dot {{ width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }}
.rname {{ font-weight: 700; flex: 1; }}
.rcat {{ font-size: 11px; color: #4a5578; }}
.footer {{ margin-top: 24px; color: #4a5578; font-size: 13px; }}
.footer strong {{ color: #6c63ff; }}
</style></head>
<body>
<h1><span>21</span> GitHub Repositories</h1>
<p class="sub">github.com/Yacinewhatchandcode</p>
<div class="grid">{cards}</div>
<p class="footer"><strong>Yacine Benhamou</strong> | Lead AI Builder | yace19ai.com</p>
</body></html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path


def main():
    print("+" + "="*58 + "+")
    print("|  Prime-AI — GitHub Repo Promo Video Generator            |")
    print("|  Generating HTML slides for all 21 repos                 |")
    print("+" + "="*58 + "+")

    slides_dir = PROMO_DIR / "slides"
    slides_dir.mkdir(exist_ok=True)

    # Generate individual slides
    for i, repo in enumerate(REPOS):
        slide_path = slides_dir / f"{i+1:02d}_{repo['name']}.html"
        generate_html_slide(repo, slide_path)
        print(f"  [{i+1:2d}/{len(REPOS)}] {repo['name']:<30s} -> {slide_path.name}")

    # Generate overview
    overview_path = slides_dir / "00_overview.html"
    create_overview_html(REPOS, overview_path)
    print(f"  [OV] Overview slide -> {overview_path.name}")

    # Generate manifest
    manifest = {
        "title": "Yace19ai.com — GitHub Portfolio",
        "author": "Yacine Benhamou",
        "website": "https://yace19ai.com",
        "github": "https://github.com/Yacinewhatchandcode",
        "total_repos": len(REPOS),
        "repos": [
            {"name": r["name"], "category": r["category"], "desc": r["desc"]}
            for r in REPOS
        ],
    }
    with open(PROMO_DIR / "repos_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\n  => {len(REPOS)} slides + 1 overview generated")
    print(f"  => Output: {PROMO_DIR}")

    # Try to open in browser for recording
    print(f"\n  To record as video:")
    print(f"  1. Run: python record_demo.py")
    print(f"  2. Or open slides manually in browser and record with OBS")
    print(f"\n  To convert slides to screenshots/video with Playwright:")
    print(f"  pip install playwright && playwright install chromium")
    print(f"  Then use record_demo.py with these slides")


if __name__ == "__main__":
    main()
