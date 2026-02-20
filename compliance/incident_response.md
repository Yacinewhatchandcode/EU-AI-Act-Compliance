# Incident Response Playbook — PRIME.AI
> GDPR Article 33–34 | Last updated: 2026-02-20

## Severity Levels

| Level | Description | Response Time | Example |
|-------|-------------|---------------|---------|
| 🔴 **Critical** | Personal data breach affecting data subjects | Immediate | Database leaked, prospect data exposed |
| 🟡 **High** | Security compromise without confirmed data breach | < 4 hours | VPS compromised, unauthorized SSH access |
| 🟢 **Medium** | Operational incident, no data exposure | < 24 hours | Agent malfunction, runaway API costs |

## Incident Response Steps

### 1. CONTAIN (0–1 hour)
```bash
# Compromised VPS
ssh root@VPS_IP
docker-compose down                    # Stop all services
ufw deny from any                      # Block all traffic except your IP
ufw allow from YOUR_IP to any port 22  # Keep SSH for yourself

# Compromised API key
# Revoke immediately in provider dashboard (Anthropic, OpenRouter)

# Compromised email
# Change Gmail password + revoke app passwords
```

### 2. ASSESS (1–4 hours)
- What data was exposed? Check `prospects.yaml`, `MEMORY.md`, `campaign_log.json`
- How many data subjects affected?
- Was the breach intentional or accidental?
- Is the vulnerability still open?

### 3. NOTIFY (within 72 hours if personal data breach)

#### CNIL Notification (GDPR Article 33)
- **Who**: CNIL — https://www.cnil.fr/fr/notifier-une-violation-de-donnees-personnelles
- **When**: Within 72 hours of becoming aware
- **What**: Nature of breach, categories of data, approximate number of subjects, consequences, measures taken
- **Skip if**: Breach is unlikely to result in risk to data subjects' rights

#### Data Subject Notification (GDPR Article 34)
- **When**: If breach likely results in HIGH risk to individuals
- **How**: Direct email to affected prospects
- **What**: Plain language description, likely consequences, measures taken, contact point

### 4. REMEDIATE
```bash
# Rotate ALL secrets
# SSH keys
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_new
# Update VPS authorized_keys

# Rebuild from clean state
docker-compose down
docker system prune -af
docker-compose build --no-cache
docker-compose up -d
```

### 5. DOCUMENT
Record in `compliance/incidents_log.csv`:
- Date/time detected
- Date/time contained
- Nature of incident
- Data affected
- Root cause
- Remediation actions
- CNIL notified (yes/no)
- Data subjects notified (yes/no)

## Prevention Checklist
- [ ] SSH key-only auth (no passwords)
- [ ] UFW firewall active with minimal ports
- [ ] Docker containers isolated
- [ ] API keys in `.env`, never in code
- [ ] `MEMORY.md` not exposed via API
- [ ] Regular security scans
- [ ] Quarterly access review
