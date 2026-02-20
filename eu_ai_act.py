#!/usr/bin/env python3
"""
EU AI Act Multi-Agent Compliance System — Core Tools
=====================================================
PRIME.AI — Leveraging EU AI Act 2024/1689 for compliance consulting.

This module provides the core tools used by the multi-agent system:
- Risk classification engine
- Compliance scoring
- Report generation
- EU AI Act knowledge base queries

Usage:
  python eu_ai_act.py classify --description "AI hiring tool that screens CVs"
  python eu_ai_act.py audit --system "PRIME.AI Visual Generator"
  python eu_ai_act.py report --type compliance --system "ChatBot Customer Service"
  python eu_ai_act.py search --query "Article 6 high risk"
"""

import json
import sys
import os
import re
from datetime import datetime, timedelta
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════
# EU AI ACT KNOWLEDGE BASE
# ═══════════════════════════════════════════════════════════════════

PROHIBITED_PRACTICES = [
    {
        "id": "P1",
        "article": "Article 5(1)(a)",
        "name": "Subliminal/manipulative AI",
        "description": "AI systems that deploy subliminal, manipulative, or deceptive techniques to distort behavior and impair informed decision-making, causing significant harm",
        "keywords": ["manipulative", "subliminal", "deceptive", "distort behavior", "dark pattern"]
    },
    {
        "id": "P2",
        "article": "Article 5(1)(b)",
        "name": "Exploitation of vulnerabilities",
        "description": "AI systems exploiting vulnerabilities due to age, disability, or social/economic situation to distort behavior causing significant harm",
        "keywords": ["vulnerable", "elderly", "children", "disability", "exploit"]
    },
    {
        "id": "P3",
        "article": "Article 5(1)(c)",
        "name": "Social scoring",
        "description": "AI systems for social scoring — evaluating or classifying persons based on social behavior or personal characteristics, leading to detrimental treatment",
        "keywords": ["social scoring", "social credit", "citizen score", "behavior scoring"]
    },
    {
        "id": "P4",
        "article": "Article 5(1)(d)",
        "name": "Criminal risk prediction",
        "description": "AI systems assessing risk of criminal offences solely based on profiling or personality traits (excluding systems supporting human assessment based on objective facts)",
        "keywords": ["predictive policing", "criminal prediction", "profiling crime", "recidivism"]
    },
    {
        "id": "P5",
        "article": "Article 5(1)(e)",
        "name": "Untargeted facial image scraping",
        "description": "AI systems creating or expanding facial recognition databases through untargeted scraping from internet or CCTV footage",
        "keywords": ["facial scraping", "face database", "biometric scraping", "clearview"]
    },
    {
        "id": "P6",
        "article": "Article 5(1)(f)",
        "name": "Emotion recognition at work/school",
        "description": "AI systems inferring emotions in workplaces or educational institutions except for medical or safety reasons",
        "keywords": ["emotion recognition", "emotion detection", "workplace emotion", "school emotion", "sentiment employee"]
    },
    {
        "id": "P7",
        "article": "Article 5(1)(g)",
        "name": "Biometric categorization (sensitive)",
        "description": "AI systems categorizing persons based on biometric data to infer race, political opinions, trade union membership, religious beliefs, sex life, or sexual orientation",
        "keywords": ["biometric categorization", "race detection", "religion detection", "political belief"]
    },
    {
        "id": "P8",
        "article": "Article 5(1)(h)",
        "name": "Real-time remote biometric ID",
        "description": "Real-time remote biometric identification in publicly accessible spaces for law enforcement (with limited exceptions)",
        "keywords": ["real-time biometric", "facial recognition public", "surveillance biometric", "live facial"]
    }
]

HIGH_RISK_CATEGORIES = [
    {
        "id": "HR1",
        "annex": "Annex III, Area 1",
        "article": "Article 6(2)",
        "name": "Biometrics",
        "description": "Remote biometric identification (not real-time), emotion recognition systems, biometric categorization",
        "keywords": ["biometric", "facial recognition", "emotion recognition", "identity verification"]
    },
    {
        "id": "HR2",
        "annex": "Annex III, Area 2",
        "article": "Article 6(2)",
        "name": "Critical infrastructure",
        "description": "Safety components of critical infrastructure: road traffic, water/gas/heating/electricity supply, digital infrastructure",
        "keywords": ["critical infrastructure", "energy", "water supply", "transport", "grid", "traffic management"]
    },
    {
        "id": "HR3",
        "annex": "Annex III, Area 3",
        "article": "Article 6(2)",
        "name": "Education & vocational training",
        "description": "AI determining access to education, evaluating learning outcomes, monitoring cheating, adaptive learning",
        "keywords": ["education", "school", "university", "exam", "grading", "student", "admission", "proctoring"]
    },
    {
        "id": "HR4",
        "annex": "Annex III, Area 4",
        "article": "Article 6(2)",
        "name": "Employment & worker management",
        "description": "CV screening, hiring decisions, promotion, termination, task allocation, monitoring, performance evaluation",
        "keywords": ["hiring", "recruitment", "CV screening", "worker", "employee", "HR", "performance review", "termination"]
    },
    {
        "id": "HR5",
        "annex": "Annex III, Area 5",
        "article": "Article 6(2)",
        "name": "Essential services access",
        "description": "Credit scoring, insurance pricing, public benefits eligibility, emergency services dispatching",
        "keywords": ["credit score", "insurance", "loan", "mortgage", "benefits", "social welfare", "emergency dispatch"]
    },
    {
        "id": "HR6",
        "annex": "Annex III, Area 6",
        "article": "Article 6(2)",
        "name": "Law enforcement",
        "description": "Evidence reliability assessment, polygraph, crime analytics, profiling, risk assessment",
        "keywords": ["law enforcement", "police", "evidence", "polygraph", "crime", "investigation", "profiling"]
    },
    {
        "id": "HR7",
        "annex": "Annex III, Area 7",
        "article": "Article 6(2)",
        "name": "Migration, asylum & border control",
        "description": "Asylum application assessment, visa decisions, border monitoring, risk assessment",
        "keywords": ["migration", "asylum", "border", "visa", "immigration", "refugee"]
    },
    {
        "id": "HR8",
        "annex": "Annex III, Area 8",
        "article": "Article 6(2)",
        "name": "Administration of justice & democracy",
        "description": "Legal research, sentencing, dispute resolution, election influence, voting systems",
        "keywords": ["justice", "court", "sentencing", "legal", "election", "voting", "judicial", "democracy"]
    }
]

COMPLIANCE_REQUIREMENTS = [
    {"id": "R1", "article": "Article 9", "name": "Risk Management System", "weight": 15},
    {"id": "R2", "article": "Article 10", "name": "Data Governance", "weight": 15},
    {"id": "R3", "article": "Article 11", "name": "Technical Documentation", "weight": 12},
    {"id": "R4", "article": "Article 12", "name": "Record-Keeping (Logging)", "weight": 10},
    {"id": "R5", "article": "Article 13", "name": "Transparency & User Info", "weight": 10},
    {"id": "R6", "article": "Article 14", "name": "Human Oversight", "weight": 15},
    {"id": "R7", "article": "Article 15", "name": "Accuracy, Robustness & Cybersecurity", "weight": 13},
    {"id": "R8", "article": "Article 43", "name": "Conformity Assessment", "weight": 5},
    {"id": "R9", "article": "Article 17", "name": "Quality Management System", "weight": 5},
]

PENALTIES = {
    "prohibited": {"max_fine_eur": 35_000_000, "max_pct": 7, "description": "Prohibited AI practices (Art. 5)"},
    "high_risk": {"max_fine_eur": 15_000_000, "max_pct": 3, "description": "High-risk AI non-compliance"},
    "misleading": {"max_fine_eur": 7_500_000, "max_pct": 1, "description": "Supplying incorrect information"},
}

DEADLINES = [
    {"date": "2025-02-02", "milestone": "Prohibitions + AI literacy obligations in force", "status": "ACTIVE"},
    {"date": "2025-08-02", "milestone": "GPAI model rules apply + governance structure", "status": "ACTIVE"},
    {"date": "2026-08-02", "milestone": "HIGH-RISK AI full compliance deadline", "status": "UPCOMING"},
    {"date": "2027-08-02", "milestone": "High-risk AI in Annex I products (safety components)", "status": "FUTURE"},
]


# ═══════════════════════════════════════════════════════════════════
# CLASSIFICATION ENGINE
# ═══════════════════════════════════════════════════════════════════

def classify_ai_system(description: str) -> dict:
    """Classify an AI system into EU AI Act risk categories."""
    desc_lower = description.lower()
    result = {
        "description": description,
        "timestamp": datetime.now().isoformat(),
        "risk_level": "MINIMAL",
        "category": "No specific regulatory category",
        "article": "N/A",
        "obligations": ["None beyond existing law"],
        "matches": []
    }

    # Check prohibited practices first
    for practice in PROHIBITED_PRACTICES:
        score = sum(1 for kw in practice["keywords"] if kw in desc_lower)
        if score >= 1:
            result["risk_level"] = "UNACCEPTABLE (PROHIBITED)"
            result["category"] = practice["name"]
            result["article"] = practice["article"]
            result["obligations"] = ["SYSTEM MUST NOT BE DEPLOYED IN THE EU"]
            result["penalty"] = PENALTIES["prohibited"]
            result["matches"].append({"type": "prohibited", "practice": practice["name"], "score": score})
            return result

    # Check high-risk categories
    for category in HIGH_RISK_CATEGORIES:
        score = sum(1 for kw in category["keywords"] if kw in desc_lower)
        if score >= 1:
            result["risk_level"] = "HIGH"
            result["category"] = category["name"]
            result["article"] = f"{category['article']} + {category['annex']}"
            result["obligations"] = [req["name"] for req in COMPLIANCE_REQUIREMENTS]
            result["penalty"] = PENALTIES["high_risk"]
            result["matches"].append({"type": "high_risk", "category": category["name"], "score": score})

    # Check limited risk (transparency obligations)
    limited_keywords = ["chatbot", "deepfake", "synthetic", "generative", "emotion recognition",
                        "virtual assistant", "ai assistant", "bot", "generated content", "AI-generated"]
    limited_score = sum(1 for kw in limited_keywords if kw in desc_lower)
    if limited_score >= 1 and result["risk_level"] == "MINIMAL":
        result["risk_level"] = "LIMITED"
        result["category"] = "Transparency obligations"
        result["article"] = "Articles 50-52"
        result["obligations"] = [
            "Disclose AI nature to users",
            "Label AI-generated content",
            "Mark deepfakes/synthetic media"
        ]

    return result


# ═══════════════════════════════════════════════════════════════════
# COMPLIANCE AUDIT ENGINE
# ═══════════════════════════════════════════════════════════════════

def run_compliance_audit(system_name: str, answers: dict = None) -> dict:
    """Run a compliance audit for a high-risk AI system."""
    audit = {
        "system_name": system_name,
        "audit_date": datetime.now().isoformat(),
        "auditor": "EU AI Act Multi-Agent System (PRIME.AI)",
        "requirements": [],
        "total_score": 0,
        "max_score": 0,
        "compliance_pct": 0,
        "rating": "",
        "priority_actions": [],
        "deadline": "2026-08-02"
    }

    for req in COMPLIANCE_REQUIREMENTS:
        status = "NOT_ASSESSED"
        score = 0
        if answers and req["id"] in answers:
            status = answers[req["id"]]
            if status == "COMPLIANT":
                score = req["weight"]
            elif status == "PARTIAL":
                score = req["weight"] * 0.5
            else:
                score = 0
                audit["priority_actions"].append({
                    "requirement": req["name"],
                    "article": req["article"],
                    "priority": "HIGH" if req["weight"] >= 13 else "MEDIUM",
                    "action": f"Implement {req['name']} as required by {req['article']}"
                })

        audit["requirements"].append({
            "id": req["id"],
            "name": req["name"],
            "article": req["article"],
            "weight": req["weight"],
            "status": status,
            "score": score
        })
        audit["max_score"] += req["weight"]
        audit["total_score"] += score

    if audit["max_score"] > 0:
        audit["compliance_pct"] = round((audit["total_score"] / audit["max_score"]) * 100, 1)

    if audit["compliance_pct"] >= 90:
        audit["rating"] = "✅ EXCELLENT — Ready for conformity assessment"
    elif audit["compliance_pct"] >= 70:
        audit["rating"] = "⚠️ GOOD — Minor gaps to address"
    elif audit["compliance_pct"] >= 50:
        audit["rating"] = "🟡 NEEDS IMPROVEMENT — Significant work required"
    else:
        audit["rating"] = "❌ NON-COMPLIANT — Major remediation needed before Aug 2026"

    return audit


# ═══════════════════════════════════════════════════════════════════
# REPORT GENERATOR
# ═══════════════════════════════════════════════════════════════════

def generate_compliance_report(system_name: str, classification: dict, audit: dict = None) -> str:
    """Generate a comprehensive compliance report in Markdown."""
    now = datetime.now()
    deadline = datetime(2026, 8, 2)
    days_remaining = (deadline - now).days

    report = f"""# 🇪🇺 EU AI Act Compliance Report
## {system_name}

**Generated**: {now.strftime('%Y-%m-%d %H:%M')}
**System**: {system_name}
**Assessed by**: PRIME.AI EU AI Act Multi-Agent Compliance System
**Regulation**: EU AI Act (Regulation (EU) 2024/1689)
**Compliance Deadline**: August 2, 2026 ({days_remaining} days remaining)

---

## 1. Executive Summary

This report assesses the compliance status of **{system_name}** against the EU AI Act.

### Risk Classification
| Attribute | Value |
|-----------|-------|
| **Risk Level** | {classification['risk_level']} |
| **Category** | {classification['category']} |
| **Legal Basis** | {classification['article']} |

### Key Obligations
"""

    for i, obligation in enumerate(classification['obligations'], 1):
        report += f"- {i}. {obligation}\n"

    if classification['risk_level'] in ['UNACCEPTABLE (PROHIBITED)']:
        report += f"""
---

## ⛔ CRITICAL WARNING

This AI system falls under **PROHIBITED PRACTICES** ({classification['article']}).

**It MUST NOT be deployed, placed on the market, or put into service in the EU.**

**Penalty**: Up to €{classification['penalty']['max_fine_eur']:,} or {classification['penalty']['max_pct']}% of global annual turnover (whichever is higher).

### Recommended Actions
1. **Immediately cease** development/deployment of this system
2. **Consult legal counsel** specialized in EU AI regulation
3. **Assess alternatives** that do not fall under prohibited practices
4. **Document** your compliance decision for regulatory records
"""

    elif classification['risk_level'] == 'HIGH':
        report += f"""
---

## 2. Compliance Deadline

⏰ **{days_remaining} days until full compliance required** (August 2, 2026)

### Key Milestones
| Date | Milestone | Status |
|------|-----------|--------|
"""
        for d in DEADLINES:
            report += f"| {d['date']} | {d['milestone']} | {d['status']} |\n"

        if audit:
            report += f"""
---

## 3. Compliance Audit Results

**Overall Score**: {audit['compliance_pct']}%
**Rating**: {audit['rating']}

### Detailed Assessment
| # | Requirement | Article | Weight | Status | Score |
|---|-------------|---------|--------|--------|-------|
"""
            for req in audit['requirements']:
                status_icon = {"COMPLIANT": "✅", "PARTIAL": "⚠️", "NON_COMPLIANT": "❌"}.get(req['status'], "ℹ️")
                report += f"| {req['id']} | {req['name']} | {req['article']} | {req['weight']} | {status_icon} {req['status']} | {req['score']} |\n"

            if audit['priority_actions']:
                report += f"""
### Priority Remediation Actions
"""
                for i, action in enumerate(audit['priority_actions'], 1):
                    report += f"**{i}. [{action['priority']}]** {action['requirement']}\n"
                    report += f"   - Article: {action['article']}\n"
                    report += f"   - Action: {action['action']}\n\n"

        report += f"""
---

## 4. Penalty Framework

| Violation Type | Max Fine | Max % Turnover |
|---------------|----------|----------------|
| Prohibited AI (Art. 5) | €35,000,000 | 7% |
| High-risk non-compliance | €15,000,000 | 3% |
| Incorrect information | €7,500,000 | 1% |

*Note: SMEs and startups benefit from proportionally lower penalties.*

---

## 5. Next Steps

1. □ Complete gap analysis for all 9 requirement areas
2. □ Establish Risk Management System (Art. 9)
3. □ Implement Data Governance framework (Art. 10)
4. □ Prepare Technical Documentation (Art. 11)
5. □ Set up automatic logging (Art. 12)
6. □ Design human oversight mechanisms (Art. 14)
7. □ Conduct conformity assessment (Art. 43)
8. □ Affix CE marking and register in EU database
9. □ Establish post-market monitoring

---

*Report generated by PRIME.AI EU AI Act Multi-Agent Compliance System*
*For questions: contact@prime-ai.fr*
"""

    return report


def generate_roadmap(system_name: str) -> str:
    """Generate a compliance roadmap."""
    now = datetime.now()
    phases = [
        {"name": "AI Inventory & Classification", "duration": 14, "tasks": [
            "Catalog all AI systems in use",
            "Classify each system by risk level",
            "Identify provider vs deployer role for each system",
            "Document intended purpose for each system"
        ]},
        {"name": "Gap Assessment", "duration": 30, "tasks": [
            "Audit current documentation against Art. 11 requirements",
            "Assess data governance practices (Art. 10)",
            "Review human oversight mechanisms (Art. 14)",
            "Evaluate logging capabilities (Art. 12)",
            "Check cybersecurity posture (Art. 15)"
        ]},
        {"name": "Risk Management System", "duration": 45, "tasks": [
            "Design risk management framework (Art. 9)",
            "Identify and document all risks",
            "Implement risk mitigation measures",
            "Set up continuous risk monitoring"
        ]},
        {"name": "Technical Implementation", "duration": 60, "tasks": [
            "Implement automatic logging system",
            "Design human oversight interfaces",
            "Set up accuracy/robustness monitoring",
            "Implement cybersecurity controls",
            "Create transparency mechanisms"
        ]},
        {"name": "Documentation & Assessment", "duration": 30, "tasks": [
            "Complete technical documentation package",
            "Prepare EU Declaration of Conformity",
            "Conduct self/third-party conformity assessment",
            "Register in EU AI database",
            "Affix CE marking"
        ]},
        {"name": "Post-Market Monitoring", "duration": 0, "tasks": [
            "Establish monitoring system for performance data",
            "Set up incident reporting procedures",
            "Plan regular compliance reviews",
            "Train staff on ongoing obligations"
        ]},
    ]

    roadmap = f"# 🗺️ EU AI Act Compliance Roadmap\n## {system_name}\n\n"
    roadmap += f"**Start Date**: {now.strftime('%Y-%m-%d')}\n"
    roadmap += f"**Compliance Deadline**: 2026-08-02\n\n"

    current_date = now
    for i, phase in enumerate(phases, 1):
        end_date = current_date + timedelta(days=phase["duration"]) if phase["duration"] > 0 else "Ongoing"
        roadmap += f"### Phase {i}: {phase['name']}\n"
        if isinstance(end_date, str):
            roadmap += f"📅 **{current_date.strftime('%Y-%m-%d')}** → {end_date}\n\n"
        else:
            roadmap += f"📅 **{current_date.strftime('%Y-%m-%d')}** → **{end_date.strftime('%Y-%m-%d')}** ({phase['duration']} days)\n\n"
            current_date = end_date

        for task in phase["tasks"]:
            roadmap += f"- [ ] {task}\n"
        roadmap += "\n"

    return roadmap


# ═══════════════════════════════════════════════════════════════════
# SELF-CHECK: OPENCLAW STACK COMPLIANCE
# ═══════════════════════════════════════════════════════════════════

OPENCLAW_COMPONENTS = [
    {
        "id": "SYS-001",
        "name": "OpenClaw Gateway",
        "description": "General-purpose AI personal assistant chatbot virtual assistant",
        "data_types": ["chat messages", "commands"],
        "gdpr_impact": "medium",
    },
    {
        "id": "SYS-002",
        "name": "EU AI Act Compliance Checker",
        "description": "Rule-based AI system classifier for risk assessment",
        "data_types": ["system descriptions"],
        "gdpr_impact": "low",
    },
    {
        "id": "SYS-003",
        "name": "Prospect Finder Pipeline",
        "description": "B2B lead generation web scraping tool",
        "data_types": ["names", "emails", "phones", "companies"],
        "gdpr_impact": "high",
    },
    {
        "id": "SYS-004",
        "name": "Email Campaign System",
        "description": "Automated B2B email outreach tool",
        "data_types": ["prospect emails", "names"],
        "gdpr_impact": "high",
    },
    {
        "id": "SYS-005",
        "name": "Desktop Control Agent",
        "description": "Automated desktop mouse keyboard screenshot tool",
        "data_types": ["screenshots"],
        "gdpr_impact": "medium",
    },
    {
        "id": "SYS-006",
        "name": "WhatsApp Integration",
        "description": "AI chatbot messaging channel virtual assistant",
        "data_types": ["messages", "phone numbers"],
        "gdpr_impact": "high",
    },
]

# Open-source alternatives for cost optimization
OPEN_SOURCE_STACK = {
    "memory": {
        "name": "Cognee",
        "repo": "https://github.com/topoteretes/cognee",
        "description": "Open-source AI memory layer — ECL pipeline (Extract, Cognify, Load). Replaces expensive vector DB services.",
        "replaces": "Pinecone, Weaviate Cloud",
        "savings": "~$50-200/mo",
    },
    "web_search": {
        "name": "Perplexica",
        "repo": "https://github.com/ItzCrazyKns/Perplexica",
        "description": "Self-hosted Perplexity alternative using SearXNG + local LLM. Free web search.",
        "replaces": "Perplexity API ($5-200/mo), Brave Search API",
        "savings": "~$20-200/mo",
    },
    "search_alt": {
        "name": "SciraAI",
        "repo": "https://github.com/Scira-ai/scira",
        "description": "Open-source AI search engine — web, academic, YouTube. 10k+ GitHub stars.",
        "replaces": "Perplexity, Google Search API",
        "savings": "~$20-100/mo",
    },
    "agent_framework": {
        "name": "OpenClaw",
        "repo": "https://github.com/openclaw/openclaw",
        "description": "Self-hosted autonomous AI agent. Already in use.",
        "replaces": "ChatGPT Plus, Claude Pro subscriptions",
        "savings": "~$20-40/mo",
    },
    "llm_local": {
        "name": "Ollama",
        "repo": "https://github.com/ollama/ollama",
        "description": "Run LLMs locally — Llama, Mistral, Gemma. Zero API cost for non-critical tasks.",
        "replaces": "OpenRouter / Anthropic API for simple tasks",
        "savings": "~$30-100/mo",
    },
    "knowledge_graph": {
        "name": "Cognee Knowledge Graphs",
        "repo": "https://github.com/topoteretes/cognee",
        "description": "Built-in knowledge graph from Cognee — connects data by meaning and relationships.",
        "replaces": "Neo4j AuraDB, custom graph solutions",
        "savings": "~$20-50/mo",
    },
}


def classify_openclaw_stack() -> dict:
    """Auto-classify all OpenClaw components and check compliance status."""
    workspace = Path(__file__).parent
    compliance_dir = workspace / "compliance"

    results = {
        "timestamp": datetime.now().isoformat(),
        "overall_status": "COMPLIANT",
        "days_to_deadline": (datetime(2026, 8, 2) - datetime.now()).days,
        "components": [],
        "compliance_docs": {},
        "gdpr_status": {},
        "open_source_alternatives": OPEN_SOURCE_STACK,
        "summary": {},
    }

    # Classify each component
    high_risk_count = 0
    for comp in OPENCLAW_COMPONENTS:
        classification = classify_ai_system(comp["description"])
        status = "✅" if classification["risk_level"] in ["MINIMAL", "LIMITED"] else "⚠️"
        if classification["risk_level"] in ["HIGH", "UNACCEPTABLE (PROHIBITED)"]:
            high_risk_count += 1
            results["overall_status"] = "ACTION_REQUIRED"

        results["components"].append({
            "id": comp["id"],
            "name": comp["name"],
            "ai_act_risk": classification["risk_level"],
            "category": classification["category"],
            "gdpr_impact": comp["gdpr_impact"],
            "data_types": comp["data_types"],
            "status_icon": status,
        })

    # Check compliance documents
    required_docs = [
        "system_register.md", "risk_register.md", "data_governance.md",
        "transparency_notice.md", "dpa_template.md", "gdpr_rights_procedures.md",
        "incident_response.md",
    ]
    docs_present = 0
    for doc in required_docs:
        exists = (compliance_dir / doc).exists()
        results["compliance_docs"][doc] = "✅" if exists else "❌"
        if exists:
            docs_present += 1

    # Check timeline
    timeline_exists = (compliance_dir / "timeline" / "roadmap_2026.md").exists()
    results["compliance_docs"]["timeline/roadmap_2026.md"] = "✅" if timeline_exists else "❌"
    if timeline_exists:
        docs_present += 1

    # Check suppression list
    suppression = (compliance_dir / "suppression_list.txt").exists()
    results["gdpr_status"]["suppression_list"] = "✅" if suppression else "⚠️ Create before next campaign"

    # Check prospects data
    prospects_file = workspace / "prospects.yaml"
    if prospects_file.exists():
        size_kb = prospects_file.stat().st_size / 1024
        results["gdpr_status"]["prospects_data"] = f"⚠️ {size_kb:.0f} KB — ensure retention policy"
    else:
        results["gdpr_status"]["prospects_data"] = "✅ No prospect data file"

    # Summary
    total_docs = len(required_docs) + 1  # +1 for timeline
    results["summary"] = {
        "total_components": len(OPENCLAW_COMPONENTS),
        "high_risk_components": high_risk_count,
        "compliance_docs_complete": f"{docs_present}/{total_docs}",
        "docs_coverage_pct": round(docs_present / total_docs * 100),
        "gdpr_significant_components": sum(1 for c in OPENCLAW_COMPONENTS if c["gdpr_impact"] == "high"),
        "estimated_monthly_savings_oss": "$140-690/mo with full open-source stack",
    }

    return results


# ═══════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1]

    if command == "classify":
        desc = " ".join(sys.argv[3:]) if len(sys.argv) > 3 and sys.argv[2] == "--description" else input("Describe your AI system: ")
        result = classify_ai_system(desc)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif command == "audit":
        name = " ".join(sys.argv[3:]) if len(sys.argv) > 3 and sys.argv[2] == "--system" else input("AI system name: ")
        result = run_compliance_audit(name)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif command == "report":
        name = " ".join(sys.argv[3:]) if len(sys.argv) > 3 and sys.argv[2] == "--system" else input("AI system name: ")
        classification = classify_ai_system(name)
        report = generate_compliance_report(name, classification)
        output_file = Path(f"report_{name.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d')}.md")
        output_file.write_text(report, encoding="utf-8")
        print(f"Report saved: {output_file}")
        print(report)

    elif command == "roadmap":
        name = " ".join(sys.argv[3:]) if len(sys.argv) > 3 and sys.argv[2] == "--system" else input("AI system name: ")
        roadmap = generate_roadmap(name)
        output_file = Path(f"roadmap_{name.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d')}.md")
        output_file.write_text(roadmap, encoding="utf-8")
        print(f"Roadmap saved: {output_file}")
        print(roadmap)

    elif command == "deadlines":
        print("\n🗓️ EU AI Act Key Deadlines:")
        for d in DEADLINES:
            days = (datetime.strptime(d["date"], "%Y-%m-%d") - datetime.now()).days
            status = "✅ IN FORCE" if days < 0 else f"⏰ {days} days"
            print(f"  {d['date']} — {d['milestone']} [{status}]")

    elif command == "search":
        query = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else input("Search query: ")
        query_lower = query.lower()
        results = []
        for p in PROHIBITED_PRACTICES:
            if query_lower in str(p).lower():
                results.append(f"🔴 PROHIBITED: {p['name']} ({p['article']})\n   {p['description']}")
        for h in HIGH_RISK_CATEGORIES:
            if query_lower in str(h).lower():
                results.append(f"🟠 HIGH RISK: {h['name']} ({h['article']}, {h['annex']})\n   {h['description']}")
        for r in COMPLIANCE_REQUIREMENTS:
            if query_lower in str(r).lower():
                results.append(f"📋 REQUIREMENT: {r['name']} ({r['article']})")

        if results:
            print(f"\n🔍 Found {len(results)} results for '{query}':\n")
            for r in results:
                print(f"  {r}\n")
        else:
            print(f"No results found for '{query}'")

    elif command == "self-check":
        result = classify_openclaw_stack()
        print("\n🛡️  OpenClaw Stack Compliance Self-Check")
        print("=" * 56)
        print(f"  Status: {result['overall_status']}")
        print(f"  Days to deadline: {result['days_to_deadline']}")
        print()
        print("  Components:")
        for c in result["components"]:
            print(f"    {c['status_icon']} {c['name']}: {c['ai_act_risk']} (GDPR: {c['gdpr_impact']})")
        print()
        print("  Compliance Docs:")
        for doc, status in result["compliance_docs"].items():
            print(f"    {status} {doc}")
        print()
        print("  GDPR Status:")
        for key, val in result["gdpr_status"].items():
            print(f"    {val}")
        print()
        print("  Open-Source Cost Savings:")
        for key, tool in result["open_source_alternatives"].items():
            print(f"    💰 {tool['name']}: {tool['savings']} — {tool['repo']}")
        print()
        s = result["summary"]
        print(f"  📊 {s['compliance_docs_complete']} docs complete ({s['docs_coverage_pct']}%)")
        print(f"  🔒 {s['high_risk_components']} high-risk | {s['gdpr_significant_components']} GDPR-significant")
        print(f"  💵 {s['estimated_monthly_savings_oss']}")

    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()
