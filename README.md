# 🇪🇺 Prime-AI — EU AI Act Compliance System

> **Scanner, classificateur et auditeur IA automatise — conforme au Reglement 2024/1689**

[![Live Demo](https://img.shields.io/badge/Live-yace19ai.com-6c63ff?style=for-the-badge)](https://yace19ai.com)
[![EU AI Act](https://img.shields.io/badge/EU%20AI%20Act-2024%2F1689-00e676?style=for-the-badge)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

---

## What is this?

**Prime-AI** is a full-stack compliance toolkit for the **EU AI Act (Regulation 2024/1689)** — the world's first comprehensive AI regulation.

It lets you:
- **Scan any URL** to detect AI systems and assess compliance risk
- **Classify AI systems** into 4 risk levels (Prohibited → Minimal)
- **Audit** against the 9 mandatory requirements (Articles 8-15)
- **Generate compliance reports** and remediation roadmaps
- **Access the complete regulatory database** (8 prohibited practices, 8 high-risk areas, 9 requirements)

All via **Web PWA, Telegram, Slack, WhatsApp, and Discord** — zero setup needed.

---

## Demo

### Dashboard with Live Countdown
The main dashboard shows real-time countdown to the compliance deadline (August 2, 2026), regulatory milestones, and quick access to all tools.

### URL Scanner
Scan any website to detect AI systems and evaluate their compliance risk level.

### AI Risk Classifier
Describe any AI system and get an instant 4-level risk classification based on the EU AI Act.

### Compliance Audit
Run a full 9-requirement audit against Articles 8-15 with weighted scoring and remediation plans.

---

## Quick Start

```bash
# Clone
git clone https://github.com/Yacinewhatchandcode/EU-AI-Act-Compliance.git
cd EU-AI-Act-Compliance

# Run (zero config needed — auto-auth in dev mode)
python eu_ai_act_server.py

# Open http://localhost:8080 — you're in!
```

**That's it.** No Google OAuth setup, no API keys, no database. The app auto-authenticates in dev mode.

---

## Architecture

```
WhatsApp / Web / CLI / Telegram / Slack / Discord
                    |
            Orchestrator (OpenClaw)
                    |
    regulatory / classifier / auditor / reporter
                    |
          eu_ai_act.py + DeepSeek V3
```

### Key Files

| File | Description |
|------|-------------|
| `eu_ai_act_server.py` | Main server — HTTP API + static files + JWT auth |
| `eu_ai_act.py` | Core compliance engine — classification, audit, scan logic |
| `web/` | PWA frontend — Material Design 3, dark mode, animations |
| `bot_engine.py` | Shared bot brain — all platforms use the same commands |
| `telegram_bot.py` | Telegram bot (@PrimeAI_bot) |
| `slack_bot.py` | Slack workspace integration |
| `whatsapp_bot.py` | WhatsApp Business Cloud API |
| `discord_bot.py` | Discord server bot |
| `landing.html` | Marketing landing page |

---

## API Endpoints

All require Bearer JWT token (auto-generated in dev mode).

| Method | Route | Description |
|--------|-------|-------------|
| `GET` | `/api/auth/dev` | Get dev JWT (auto-auth) |
| `GET` | `/api/auth/status` | Check auth status |
| `POST` | `/api/classify` | Classify AI system risk |
| `POST` | `/api/audit` | Run 9-requirement audit |
| `POST` | `/api/report` | Generate compliance report |
| `GET` | `/api/scan?url=...` | Scan URL for AI compliance |
| `GET` | `/api/stats` | Get regulatory stats |
| `POST` | `/api/roadmap` | Generate compliance roadmap |
| `GET` | `/api/search?q=...` | Search regulatory database |

---

## EU AI Act Quick Reference

### Prohibited Practices (Article 5)
| # | Practice | Article |
|---|----------|---------|
| P1 | Subliminal/manipulative AI | 5(1)(a) |
| P2 | Exploitation of vulnerabilities | 5(1)(b) |
| P3 | Social scoring | 5(1)(c) |
| P4 | Criminal risk prediction | 5(1)(d) |
| P5 | Untargeted facial scraping | 5(1)(e) |
| P6 | Emotion recognition at work/school | 5(1)(f) |
| P7 | Biometric categorization (sensitive) | 5(1)(g) |
| P8 | Real-time remote biometric ID | 5(1)(h) |

### High-Risk Categories (Annex III)
| Area | Examples |
|------|----------|
| Biometrics | Remote ID, emotion recognition |
| Critical infrastructure | Traffic, energy, water, digital |
| Education | Access, evaluation, adaptive learning |
| Employment | CV screening, hiring, monitoring |
| Essential services | Credit, insurance, public benefits |
| Law enforcement | Evidence, profiling, risk assessment |
| Migration | Asylum, visa, border control |
| Justice & democracy | Legal research, elections |

### Sanctions
- **35M EUR / 7% revenue** — Prohibited AI violations
- **15M EUR / 3% revenue** — High-risk non-compliance
- **7.5M EUR / 1% revenue** — Providing false information

---

## Platform Bots

### Telegram
```bash
export TELEGRAM_BOT_TOKEN="your-token"
python telegram_bot.py
# Commands: /classify, /scan, /audit, /roadmap, /deadlines, /pricing
```

### Slack
```bash
export SLACK_BOT_TOKEN="xoxb-your-token"
python slack_bot.py
```

### Discord
```bash
export DISCORD_BOT_TOKEN="your-token"
python discord_bot.py
```

### All at once
```bash
python start_all_bots.py
```

---

## Tech Stack

- **Backend**: Python 3.10+ (stdlib only — zero dependencies)
- **Frontend**: Vanilla HTML/CSS/JS, Material Design 3, PWA
- **Auth**: JWT (HMAC-SHA256), Google OAuth 2.0 (optional)
- **AI**: DeepSeek V3 via OpenRouter (optional)
- **Bots**: Telegram, Slack, WhatsApp, Discord APIs

---

## Roadmap

- [x] Core classification engine (4 risk levels)
- [x] URL scanner with AI detection
- [x] 9-requirement audit (Art. 8-15)
- [x] Report generator
- [x] Compliance roadmap
- [x] Knowledge base (complete regulation)
- [x] PWA with Material Design 3
- [x] JWT authentication (zero-config)
- [x] Multi-platform bots
- [x] Marketing landing page
- [ ] Google OAuth production setup
- [ ] PDF report export
- [ ] Multi-language (EN/FR/DE/ES)
- [ ] Enterprise admin dashboard
- [ ] Webhook notifications

---

## Author

**Yacine Benhamou** — Lead AI Builder
- Website: [yace19ai.com](https://yace19ai.com)
- GitHub: [@Yacinewhatchandcode](https://github.com/Yacinewhatchandcode)
- LinkedIn: [yacine-benhamou](https://linkedin.com/in/yacine-benhamou-b26386124)

---

## License

MIT License — See [LICENSE](LICENSE) for details.

---

<p align="center">
  <strong>Made with care in Europe 🇪🇺</strong><br>
  <em>Helping organizations comply with the world's first AI regulation</em>
</p>
