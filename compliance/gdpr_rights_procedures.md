# GDPR Data Subject Rights — Operating Procedures
> GDPR Articles 15–22 | Last updated: 2026-02-20

## Receiving a Request

1. Requests arrive via **info.primeai@gmail.com**
2. Log the request in `compliance/requests_log.csv` (date, type, requester, status)
3. Verify identity (ask for name + email used to confirm match in `prospects.yaml`)
4. Respond within **30 calendar days**

## Procedure by Request Type

### Access Request (Article 15)
```
1. Search prospects.yaml for the requester's name/email
2. Search campaign_log.json for any email records
3. Search OpenClaw session logs for any mentions
4. Compile all data into a single document
5. Send to requester as PDF or structured text
```

### Rectification (Article 16)
```
1. Locate the record in prospects.yaml
2. Update the incorrect fields
3. Confirm changes to the requester
4. Log the change with timestamp
```

### Erasure / Right to be Forgotten (Article 17)
```
1. Delete from prospects.yaml
2. Delete from campaign_log.json
3. Search and purge from OpenClaw session logs
4. Remove from any email lists
5. Confirm deletion to the requester
6. Retain only the erasure request itself (legal obligation)
```

### Objection to Direct Marketing (Article 21)
```
1. This is an ABSOLUTE right — no balancing test needed
2. Immediately remove from prospects.yaml
3. Add to suppression list (compliance/suppression_list.txt)
4. Confirm to the requester within 48 hours
5. Check suppression list BEFORE any future campaign
```

## Suppression List

Maintain `compliance/suppression_list.txt` — one email per line. Check this **before every campaign send**.

## Response Templates

### Acknowledgment
> Thank you for your request regarding your personal data. We will process your request within 30 days as required by GDPR Article 12. If you have any questions, contact info.primeai@gmail.com.

### Completion
> We have completed your [access/erasure/rectification] request. [Details of action taken]. If you have further questions, please don't hesitate to contact us.

## Escalation
If a request cannot be fulfilled (e.g., legal obligation to retain), document the reason and inform the requester of their right to lodge a complaint with the **CNIL** (Commission nationale de l'informatique et des libertés).
