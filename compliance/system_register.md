# AI System Register — PRIME.AI / OpenClaw
> EU AI Act Article 49 | Last updated: 2026-02-20

## Operator Information
| Field | Value |
|-------|-------|
| **Operator** | PRIME.AI |
| **Location** | France (EU) |
| **Contact** | info.primeai@gmail.com |
| **Role** | Deployer (Article 3(4)) |

---

## System Inventory

### SYS-001: OpenClaw Gateway (Personal Assistant)
| Field | Value |
|-------|-------|
| **Purpose** | General-purpose personal AI assistant |
| **AI Models** | Llama 3.3 70B (OpenRouter), Claude Opus 4.6 (Anthropic) |
| **Users** | Single operator (personal use) |
| **Data Types** | Chat messages, commands, task context |
| **Annex III Domain** | ❌ None |
| **Risk Level** | **Low-risk / General Purpose** |
| **Transparency** | Article 50 — users informed of AI interaction |
| **Hosting** | Hostinger VPS (EU / Lithuania) |

### SYS-002: EU AI Act Compliance Checker
| Field | Value |
|-------|-------|
| **Purpose** | Classify AI systems and audit compliance |
| **AI Models** | Rule-based (no LLM) |
| **Users** | PRIME.AI clients |
| **Data Types** | System descriptions, audit answers |
| **Annex III Domain** | ❌ None |
| **Risk Level** | **Low-risk** |
| **Hosting** | Hostinger VPS (EU / Lithuania) |

### SYS-003: Prospect Finder Pipeline
| Field | Value |
|-------|-------|
| **Purpose** | B2B lead generation for PRIME.AI consulting |
| **AI Models** | None (web scraping + enrichment) |
| **Users** | PRIME.AI operator |
| **Data Types** | ⚠️ Names, emails, phone numbers, companies, LinkedIn URLs |
| **Annex III Domain** | ❌ None |
| **Risk Level** | **Low-risk** (AI Act) / **High GDPR impact** |
| **Legal Basis (GDPR)** | Legitimate interest (Art. 6(1)(f)) — B2B direct marketing |
| **Retention** | 12 months max, reviewed quarterly |

### SYS-004: Email Campaign System
| Field | Value |
|-------|-------|
| **Purpose** | Automated B2B outreach emails |
| **AI Models** | None (template-based) |
| **Users** | PRIME.AI operator |
| **Data Types** | ⚠️ Prospect emails, names, companies |
| **Annex III Domain** | ❌ None |
| **Risk Level** | **Low-risk** (AI Act) / **High GDPR impact** |
| **Legal Basis (GDPR)** | Legitimate interest (Art. 6(1)(f)) with opt-out |

### SYS-005: Desktop Control Agent
| Field | Value |
|-------|-------|
| **Purpose** | Automated desktop actions (screenshots, clicks, typing) |
| **AI Models** | LLM-directed (via OpenClaw) |
| **Users** | Single operator |
| **Data Types** | Screenshots (may contain sensitive info) |
| **Annex III Domain** | ❌ None |
| **Risk Level** | **Low-risk** |
| **Note** | Screenshots not stored persistently, overwritten each call |

### SYS-006: WhatsApp Integration
| Field | Value |
|-------|-------|
| **Purpose** | Agent communication channel |
| **AI Models** | LLM-powered responses via OpenClaw |
| **Users** | Single operator (selfChatMode) |
| **Data Types** | ⚠️ Messages, phone numbers, media |
| **Annex III Domain** | ❌ None |
| **Risk Level** | **Low-risk** (AI Act) / **Medium GDPR** |
| **Transparency** | Self-use only — no third-party exposure |

---

## Classification Summary

| Category | Count |
|----------|-------|
| **Prohibited** | 0 |
| **High-risk (Annex III)** | 0 |
| **Limited-risk (transparency)** | 2 (SYS-001, SYS-006) |
| **Low-risk** | 6 |
| **GDPR-significant** | 3 (SYS-003, SYS-004, SYS-006) |

> **Conclusion**: No conformity assessment or CE marking required. Focus compliance effort on GDPR for prospecting pipeline and AI Act Article 50 transparency.
