# Risk Register — PRIME.AI / OpenClaw
> Version 1.0 | Last updated: 2026-02-20

## Risk Matrix

| ID | Threat | Severity | Likelihood | Impact | Mitigation | Status |
|----|--------|----------|------------|--------|------------|--------|
| R-01 | **Prompt injection** — malicious input manipulates agent behavior | 🔴 High | Medium | Agent executes unintended actions | Sandbox tool execution, input validation, SOUL.md boundaries | ⚠️ Partial |
| R-02 | **Data exfiltration** — agent leaks personal data via API calls | 🔴 High | Low | GDPR breach, fines up to €20M | Restrict outbound API calls, audit logs, no MEMORY.md in API | ⚠️ Partial |
| R-03 | **Email abuse** — campaign system sends spam / exceeds limits | 🟡 Medium | Medium | Domain blacklisted, GDPR complaint | Rate limiting in `email_campaign.py`, opt-out link, consent records | ⚠️ Partial |
| R-04 | **Credential leak** — API keys exposed in logs or code | 🔴 High | Low | Unauthorized API usage, financial loss | `.env` files, never hardcode keys, git-ignore secrets | ✅ Done |
| R-05 | **Over-automation** — agent takes irreversible actions without approval | 🟡 Medium | Medium | Unintended emails/purchases/deletions | Human approval for external actions (SOUL.md rule) | ✅ Done |
| R-06 | **Prospect data staleness** — outdated contact info in `prospects.yaml` | 🟡 Medium | High | Emails to wrong people, GDPR issue | Quarterly data review, retention policy (12 months) | ❌ TODO |
| R-07 | **VPS compromise** — unauthorized SSH access | 🔴 High | Low | Full system takeover | SSH key auth, firewall (UFW), fail2ban, Docker isolation | ⚠️ Partial |
| R-08 | **Screenshot data exposure** — `screenshot.png` captures sensitive content | 🟡 Medium | Medium | Unintended disclosure of on-screen data | Auto-overwrite, no persistent storage, no API exposure | ✅ Done |
| R-09 | **LLM hallucination in compliance advice** — wrong classification | 🟡 Medium | Medium | Client receives incorrect legal guidance | Rule-based classifier (no LLM), human review recommended | ✅ Done |
| R-10 | **Token/cost runaway** — LLM API costs spiral | 🟡 Medium | Medium | Unexpected bills | OpenRouter budget limits, `/compact` usage, Haiku for heartbeat | ⚠️ Partial |

## Risk Appetite
- **Zero tolerance**: Data breaches, unauthorized external communications
- **Low tolerance**: Security vulnerabilities, compliance gaps
- **Moderate tolerance**: Cost overruns, minor automation errors

## Review Schedule
- **Monthly**: Review R-01, R-02, R-07 (security risks)
- **Quarterly**: Full register review + prospect data purge (R-06)
- **On change**: Any new tool, channel, or API integration triggers re-assessment
