<p align="center">
  <img src="web/prime-ai-logo.svg" width="80" alt="Prime-AI Logo">
</p>

<h1 align="center">🇪🇺 Prime-AI — EU AI Act Compliance System</h1>

<p align="center">
  <strong>The first open-source toolkit to scan, classify, audit, and report AI systems under EU Regulation 2024/1689</strong>
</p>

<p align="center">
  <a href="https://yace19ai.com"><img src="https://img.shields.io/badge/Live-yace19ai.com-6c63ff?style=for-the-badge" /></a>
  <a href="https://eur-lex.europa.eu/eli/reg/2024/1689/oj"><img src="https://img.shields.io/badge/EU%20AI%20Act-2024%2F1689-00e676?style=for-the-badge" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" /></a>
  <a href="#quick-start"><img src="https://img.shields.io/badge/Setup-Zero%20Config-ff9100?style=for-the-badge" /></a>
</p>

<p align="center">
  <a href="https://github.com/Yacinewhatchandcode/EU-AI-Act-Compliance/stargazers"><img src="https://img.shields.io/github/stars/Yacinewhatchandcode/EU-AI-Act-Compliance?style=social" /></a>
  <a href="https://github.com/Yacinewhatchandcode/EU-AI-Act-Compliance/network/members"><img src="https://img.shields.io/github/forks/Yacinewhatchandcode/EU-AI-Act-Compliance?style=social" /></a>
</p>

---

## 🎬 Product Demo

<p align="center">
  <a href="https://github.com/Yacinewhatchandcode/EU-AI-Act-Compliance/raw/main/demo_videos/PRIME_AI_30s.mp4">
    <img src="https://img.shields.io/badge/▶%20Watch%20Demo-30s%20Fast%20Preview-6c63ff?style=for-the-badge&logo=youtube" />
  </a>
  <a href="https://github.com/Yacinewhatchandcode/EU-AI-Act-Compliance/raw/main/demo_videos/PRIME_AI_PROMO.mp4">
    <img src="https://img.shields.io/badge/▶%20Full%20Walkthrough-90s%20Complete%20Demo-00e676?style=for-the-badge&logo=youtube" />
  </a>
</p>

https://github.com/Yacinewhatchandcode/EU-AI-Act-Compliance/raw/main/demo_videos/PRIME_AI_30s.mp4

> **6 use cases recorded** — Landing Page • Auto-Login • Risk Classifier • URL Scanner • 9-Requirement Audit • Knowledge Base

---

## 💡 What is this?

**Prime-AI** is a full-stack compliance toolkit for the **EU AI Act (Regulation 2024/1689)** — the world's first comprehensive AI regulation, effective **August 2, 2026**.

| Feature | Description |
|---------|-------------|
| 🔍 **URL Scanner** | Scan any website to detect AI systems and assess compliance risk |
| ⚖️ **Risk Classifier** | Classify AI systems into 4 levels: Prohibited → High → Limited → Minimal |
| 📋 **9-Requirement Audit** | Full audit against Articles 8-15 with weighted scoring |
| 📊 **Compliance Reports** | Generate reports with remediation roadmaps |
| 📚 **Knowledge Base** | Complete regulatory database — 8 prohibited, 8 high-risk, 9 requirements |
| 🤖 **Multi-Platform** | Web PWA + Telegram + Slack + WhatsApp + Discord |

---

## ⚡ Quick Start

```bash
# Clone
git clone https://github.com/Yacinewhatchandcode/EU-AI-Act-Compliance.git
cd EU-AI-Act-Compliance

# Install (optional — stdlib only, zero mandatory deps)
pip install -r requirements.txt  # only if you want AI-powered analysis

# Run
python eu_ai_act_server.py

# Open → http://localhost:8080
```

**That's it.** Zero config required. Auto-login in dev mode. No database. No API keys needed.

---

## 🎯 Use Cases — All Recorded as Video

| # | Use Case | Video | Duration |
|---|----------|-------|----------|
| 1 | **Marketing Landing Page** | [`uc1_landing.mp4`](demo_videos/uc1_landing.mp4) | ~20s |
| 2 | **Zero-Click Auto Login** | [`uc2_auto_login.mp4`](demo_videos/uc2_auto_login.mp4) | ~11s |
| 3 | **AI Risk Classifier** | [`uc3_classifier.mp4`](demo_videos/uc3_classifier.mp4) | ~14s |
| 4 | **URL Compliance Scanner** | [`uc4_scanner.mp4`](demo_videos/uc4_scanner.mp4) | ~14s |
| 5 | **9-Requirement Audit** | [`uc5_audit.mp4`](demo_videos/uc5_audit.mp4) | ~14s |
| 6 | **Knowledge Base Browse** | [`uc6_kb.mp4`](demo_videos/uc6_kb.mp4) | ~12s |

> All demos recorded autonomously using Playwright. See [`record_demo.py`](record_demo.py).

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│              Client Layer (PWA / Bots)              │
│   Web App  ·  Telegram  ·  Slack  ·  WhatsApp  ·  Discord │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP / WebSocket
┌──────────────────────┴──────────────────────────────┐
│              eu_ai_act_server.py (API)              │
│   JWT Auth  ·  REST API  ·  Static Files            │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────┐
│              eu_ai_act.py (Core Engine)             │
│   Classifier  ·  Auditor  ·  Scanner  ·  Reporter  │
│   Regulatory DB  ·  Risk Matrix  ·  Remediation     │
└─────────────────────────────────────────────────────┘
```

### Project Structure

```
EU-AI-Act-Compliance/
├── eu_ai_act_server.py    # HTTP API server + JWT auth
├── eu_ai_act.py           # Core compliance engine
├── bot_engine.py          # Shared bot command brain
├── web/                   # PWA frontend
│   ├── index.html         # Main app (Material Design 3)
│   ├── landing.html       # Marketing landing page
│   ├── login.html         # Auth page (auto-login capable)
│   ├── app.js             # Client-side logic
│   ├── style.css          # Premium dark theme
│   └── manifest.json      # PWA manifest
├── compliance/            # GDPR & EU AI Act compliance docs
├── deploy/                # Docker + VPS deployment configs
├── demo_videos/           # 6 use case recordings + promo
│   ├── PRIME_AI_30s.mp4   # 30s fast marketing video
│   └── PRIME_AI_PROMO.mp4 # 90s full walkthrough
├── telegram_bot.py        # Telegram integration
├── slack_bot.py           # Slack integration
├── discord_bot.py         # Discord integration
└── whatsapp_bot.py        # WhatsApp integration
```

---

## 🔌 API Reference

All endpoints require `Authorization: Bearer <token>` (auto-generated in dev mode).

| Method | Endpoint | Body | Description |
|--------|----------|------|-------------|
| `GET` | `/api/auth/dev` | — | Get dev JWT token |
| `GET` | `/api/auth/status` | — | Verify authentication |
| `POST` | `/api/classify` | `{ "description": "..." }` | Classify AI risk level |
| `POST` | `/api/audit` | `{ "name": "...", "scores": [...] }` | Run 9-requirement audit |
| `GET` | `/api/scan?url=...` | — | Scan URL for compliance |
| `POST` | `/api/report` | `{ "audit_id": "..." }` | Generate report |
| `POST` | `/api/roadmap` | `{ "classification": "..." }` | Compliance roadmap |
| `GET` | `/api/stats` | — | Regulatory statistics |
| `GET` | `/api/search?q=...` | — | Search regulation |
| `GET` | `/api/knowledge` | — | Full regulatory database |

---

## ⚖️ EU AI Act Quick Reference

### Risk Levels
| Level | Color | Examples | Obligation |
|-------|-------|----------|------------|
| 🔴 **Prohibited** | Red | Social scoring, subliminal manipulation | **Banned** |
| 🟠 **High-Risk** | Orange | CV screening, credit scoring, biometrics | Full compliance (Art. 8-15) |
| 🟡 **Limited** | Yellow | Chatbots, emotion recognition | Transparency obligations |
| 🟢 **Minimal** | Green | Spam filters, video games | Voluntary codes |

### 9 Mandatory Requirements (High-Risk AI)
| # | Requirement | Article |
|---|-------------|---------|
| R1 | Risk Management System | Art. 9 |
| R2 | Data Governance | Art. 10 |
| R3 | Technical Documentation | Art. 11 |
| R4 | Record-Keeping | Art. 12 |
| R5 | Transparency | Art. 13 |
| R6 | Human Oversight | Art. 14 |
| R7 | Accuracy & Robustness | Art. 15 |
| R8 | Cybersecurity | Art. 15 |
| R9 | Quality Management | Art. 17 |

### Sanctions
| Violation | Fine |
|-----------|------|
| Prohibited AI | **€35M** or 7% global revenue |
| High-risk non-compliance | **€15M** or 3% global revenue |
| False information | **€7.5M** or 1% global revenue |

---

## 🤖 Platform Bots

```bash
# Telegram
export TELEGRAM_BOT_TOKEN="your-token"
python telegram_bot.py

# Slack
export SLACK_BOT_TOKEN="xoxb-your-token"
python slack_bot.py

# Discord
export DISCORD_BOT_TOKEN="your-token"
python discord_bot.py

# All at once
python start_all_bots.py
```

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.10+ (stdlib only — zero mandatory deps) |
| **Frontend** | Vanilla HTML/CSS/JS, Material Design 3, PWA |
| **Auth** | JWT (HMAC-SHA256), Google OAuth 2.0 (optional) |
| **AI Engine** | DeepSeek V3 via OpenRouter (optional) |
| **Deployment** | Docker, Nginx, Let's Encrypt |
| **Bots** | Telegram, Slack, WhatsApp Cloud, Discord APIs |

---

## 📅 Roadmap

- [x] Core classification engine (4 risk levels)
- [x] URL scanner with AI detection
- [x] 9-requirement audit (Articles 8-15)
- [x] Compliance report generator
- [x] Compliance roadmap builder
- [x] Knowledge base (complete regulation)
- [x] PWA with Material Design 3
- [x] JWT authentication (zero-config dev mode)
- [x] Multi-platform bots (Telegram, Slack, Discord, WhatsApp)
- [x] Marketing landing page
- [x] Automated demo video recording
- [ ] Google OAuth production setup
- [ ] PDF/DOCX report export
- [ ] Multi-language support (EN/FR/DE/ES/IT)
- [ ] Enterprise admin dashboard
- [ ] Webhook notifications
- [ ] CI/CD pipeline

---

## 🚀 Deployment

See [`deploy/README.md`](deploy/README.md) for Docker + VPS deployment.

```bash
# Quick Docker deploy
docker compose -f deploy/docker-compose.yml up -d

# With HTTPS
./deploy/enable_https.sh your-domain.com
```

---

## 👤 Author

**Yacine Benhamou** — AI Builder & EU Tech Compliance

<p>
  <a href="https://yace19ai.com"><img src="https://img.shields.io/badge/Portfolio-yace19ai.com-6c63ff?style=flat-square&logo=safari" /></a>
  <a href="https://github.com/Yacinewhatchandcode"><img src="https://img.shields.io/badge/GitHub-Yacinewhatchandcode-181717?style=flat-square&logo=github" /></a>
  <a href="https://linkedin.com/in/yacine-benhamou-b26386124"><img src="https://img.shields.io/badge/LinkedIn-Yacine%20Benhamou-0A66C2?style=flat-square&logo=linkedin" /></a>
  <a href="https://prime-ai.fr"><img src="https://img.shields.io/badge/Prime--AI-prime--ai.fr-00e676?style=flat-square" /></a>
</p>

---

## 📄 License

MIT License — See [LICENSE](LICENSE) for details.

---

<p align="center">
  <strong>Made with 🇪🇺 in Europe</strong><br>
  <em>The first open-source compliance toolkit for the world's first AI regulation</em><br><br>
  <a href="https://github.com/Yacinewhatchandcode/EU-AI-Act-Compliance/stargazers">⭐ Star this repo</a> · 
  <a href="https://github.com/Yacinewhatchandcode/EU-AI-Act-Compliance/issues">🐛 Report Bug</a> · 
  <a href="https://github.com/Yacinewhatchandcode/EU-AI-Act-Compliance/issues">💡 Request Feature</a>
</p>
