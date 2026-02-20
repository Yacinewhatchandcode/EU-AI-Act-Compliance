# Data Governance — PRIME.AI / OpenClaw
> GDPR Articles 5, 6, 13, 14, 30 | Last updated: 2026-02-20

## Data Flow Map

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Web Scraping    │────▶│  prospects.yaml  │────▶│ email_campaign  │
│  prospect_finder │     │  (72 KB, ~200+   │     │  .py            │
│  .py             │     │   contacts)      │     │  SMTP outbound  │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                              │
                              ▼
                        ┌──────────────┐
                        │ enrich_      │
                        │ prospects.py │
                        │ (adds email, │
                        │  phone, web) │
                        └──────────────┘

┌─────────────────┐     ┌──────────────────┐
│  WhatsApp        │────▶│  MEMORY.md       │
│  Messages        │     │  (user profile)  │
└─────────────────┘     └──────────────────┘

┌─────────────────┐     ┌──────────────────┐
│  Chat / Gateway  │────▶│  OpenClaw logs   │
│  Prompts         │     │  (sessions/)     │
└─────────────────┘     └──────────────────┘
```

## Personal Data Inventory

| Data Store | Personal Data | Data Subjects | Legal Basis | Retention |
|------------|--------------|---------------|-------------|-----------|
| `prospects.yaml` | Name, email, phone, company, LinkedIn | B2B prospects (France) | Legitimate interest Art. 6(1)(f) | 12 months |
| `MEMORY.md` | Operator name, phone, location | Operator (self) | Consent (self-data) | Indefinite |
| `USER.md` | Name, timezone, preferences | Operator (self) | Consent (self-data) | Indefinite |
| WhatsApp messages | Message content, phone numbers | Operator + contacts | Legitimate interest | Session-based |
| OpenClaw sessions | Chat logs, prompts, responses | Operator | Legitimate interest | 30 days |
| `campaign_log.json` | Email addresses, send status | B2B prospects | Legitimate interest | 12 months |
| `screenshot.png` | Screen content (transient) | Operator | Consent (self) | Overwritten each use |

## Legitimate Interest Assessment (Prospecting)

### Purpose
B2B direct marketing for PRIME.AI EU AI Act consulting services.

### Necessity
Direct outreach to businesses that may need AI compliance assistance before the August 2026 deadline. No less intrusive means available for reaching decision-makers.

### Balancing Test
| Factor | Assessment |
|--------|-----------|
| **Operator interest** | Strong — core business activity |
| **Data subjects' expectations** | B2B contacts expect professional outreach |
| **Nature of data** | Business contact info (not sensitive) |
| **Impact on data subjects** | Minimal — easy opt-out provided |
| **Safeguards** | Opt-out in every email, data purge quarterly |

**Conclusion**: Legitimate interest is valid. Safeguards adequate.

## Data Subject Rights Procedures

| Right | How to Exercise | Response Time |
|-------|----------------|---------------|
| **Access** (Art. 15) | Email info.primeai@gmail.com | 30 days |
| **Rectification** (Art. 16) | Email request → update `prospects.yaml` | 30 days |
| **Erasure** (Art. 17) | Email request → delete from YAML + logs | 30 days |
| **Restriction** (Art. 18) | Email request → flag record, stop processing | 30 days |
| **Portability** (Art. 20) | Export prospect data as CSV | 30 days |
| **Objection** (Art. 21) | Opt-out link in emails → auto-removal | Immediate |

## Deletion Procedures

### Prospect Data
```bash
# Remove a specific contact from prospects.yaml
python -c "
import yaml
with open('prospects.yaml') as f:
    data = yaml.safe_load(f)
# Filter out by name or email
# Save back
"
```

### Session Logs
```bash
# Clear OpenClaw sessions
rm -rf ~/.openclaw/agents/*/sessions/*
```

### Full Data Purge
```bash
# Nuclear option — remove all personal data
rm prospects.yaml campaign_log.json
# Reset MEMORY.md to template
```

## Data Processing Agreements Required

| Processor | Service | DPA Status |
|-----------|---------|-----------|
| **Hostinger** | VPS hosting (EU/Lithuania) | ⬜ Pending — request via support |
| **OpenRouter** | LLM API relay | ⬜ Pending — check terms |
| **Anthropic** | Claude API | ⬜ Pending — review DPA |
| **Gmail/Google** | SMTP for campaigns | ✅ Google Workspace DPA |

## Data Protection Impact Assessment (DPIA)

**Required?** No — processing does not meet the threshold for mandatory DPIA (no large-scale profiling, no sensitive data, no systematic monitoring of public areas).

**Voluntary DPIA recommended?** Yes, for the prospecting pipeline when scaling beyond 1,000 contacts.
