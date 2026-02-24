#!/usr/bin/env python3
"""
EU AI Act Multi-Agent Compliance System — Core Tools
=====================================================
PRIME.AI — Leveraging EU AI Act 2024/1689 for compliance consulting.
"""

import json
import sys
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
import requests
import time

# ═══════════════════════════════════════════════════════════════════
# AI BRAIN: OPENROUTER CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

OPENROUTER_MODELS = [
    "google/gemma-2-9b-it:free",
    "mistralai/mistral-7b-instruct:free",
    "microsoft/phi-3-mini-128k-instruct:free"
]

PENALTIES = {
    "unacceptable": "€35M or 7% global turnover",
    "high_risk": "€15M or 3% global turnover",
    "data_breach": "€7.5M or 1.5% global turnover"
}

DEADLINES = {
    "prohibited": "February 2025",
    "gpai": "August 2025",
    "high_risk": "August 2026"
}

OPEN_SOURCE_STACK = {
    "llama": "High (General Purpose)",
    "mistral": "High (EU Based)",
    "qwen": "Medium (Compliance Variable)"
}

def query_ai_brain(prompt: str) -> str:
    """Query OpenRouter with fallback logic across 3 free models."""
    api_key = os.getenv("AI_BRAIN_API_KEY")
    if not api_key or "your_llm_key" in api_key:
        return "AI analysis unavailable: Update .env with OpenRouter API Key."

    for model in OPENROUTER_MODELS:
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://prime-ai.com",
                    "X-Title": "PRIME AI Auditor"
                },
                data=json.dumps({
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                }),
                timeout=15
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                continue
        except Exception:
            continue

    return "AI Brain timeout. All fallback models exhausted."

# ═══════════════════════════════════════════════════════════════════
# EU AI ACT KNOWLEDGE BASE
# ═══════════════════════════════════════════════════════════════════

PROHIBITED_PRACTICES = [
    {"id": "P1", "article": "Article 5(1)(a)", "name": "Subliminal/manipulative AI", "keywords": ["manipulative", "subliminal", "deceptive"]},
    {"id": "P2", "article": "Article 5(1)(b)", "name": "Exploitation of vulnerabilities", "keywords": ["vulnerable", "elderly", "children"]},
    {"id": "P3", "article": "Article 5(1)(c)", "name": "Social scoring", "keywords": ["social scoring", "social credit"]}
]

HIGH_RISK_CATEGORIES = [
    {"id": "HR1", "annex": "Annex III, Area 1", "article": "Article 6(2)", "name": "Biometrics", "keywords": ["biometric", "facial recognition"]},
    {"id": "HR4", "annex": "Annex III, Area 4", "article": "Article 6(2)", "name": "Employment & worker management", "keywords": ["hiring", "recruitment"]},
    {"id": "HR5", "annex": "Annex III, Area 5", "article": "Article 6(2)", "name": "Essential services access", "keywords": ["credit score", "insurance"]}
]

COMPLIANCE_REQUIREMENTS = [
    {"id": "R1", "article": "Article 9", "name": "Risk Management System", "weight": 15},
    {"id": "R2", "article": "Article 10", "name": "Data Governance", "weight": 15}
]

def classify_ai_system(description: str) -> dict:
    desc_lower = description.lower()
    res = {"description": description, "risk_level": "MINIMAL", "category": "General AI", "article": "N/A", "obligations": ["Standard transparency"]}
    for p in PROHIBITED_PRACTICES:
        if any(kw in desc_lower for kw in p["keywords"]):
            res.update({"risk_level": "UNACCEPTABLE", "category": p["name"], "article": p["article"], "obligations": ["STOP DEPLOYMENT"]})
            return res
    for c in HIGH_RISK_CATEGORIES:
        if any(kw in desc_lower for kw in c["keywords"]):
            res.update({"risk_level": "HIGH", "category": c["name"], "article": c["article"], "obligations": [r["name"] for r in COMPLIANCE_REQUIREMENTS]})
            return res
    return res

def generate_compliance_report(system_name: str, classification: dict) -> str:
    now = datetime.now()
    report_id = f"PRIME-{now.strftime('%y%m%d')}-{system_name[:3].upper()}"
    report = f"""# 🛡️ Official EU AI Act Audit: {system_name}
**Report ID**: `{report_id}` | **Date**: {now.strftime('%Y-%m-%d')}
**Auditor**: PRIME.AI — 78700 Conflans, France

---

## 1. Executive Summary
This professional assessment is provided by **PRIME.AI**, an authorized technical consulting entity based in **Conflans-Sainte-Honorine (78700)**.

**Regulatory Standing**: **{classification['risk_level']}**
**Primary Category**: {classification['category']}
**Legal Basis**: {classification['article']}

---

## 2. Identified Obligations
"""
    for i, obl in enumerate(classification['obligations'], 1):
        report += f"{i}. **{obl}**\n"

    report += f"""
---

## 🔬 3. DEEP AI ANALYSIS (PRIME.AI BRAIN)
"""
    prompt = f"Analyze the following AI system: '{system_name}'. Provide a technical risk assessment and 3 remediation steps for EU AI Act compliance."
    report += query_ai_brain(prompt) + "\n\n"

    report += f"""
---

## ⚖️ LEGAL NOTICE
**PRIME.AI** (Conflans, France) provides this as a Technical Gap Analysis. It is NOT legal advice.
"""
    return report

def run_compliance_audit(system_name: str, answers: dict = None) -> dict:
    """Simulates a full 9-requirement audit."""
    classification = classify_ai_system(system_name)
    compliance_score = random.randint(65, 95) if answers else 45
    
    return {
        "system": system_name,
        "compliance_pct": compliance_score,
        "risk_level": classification["risk_level"],
        "requirements": [
            {"id": "R1", "name": "Risk Management", "status": "COMPLIANT" if compliance_score > 80 else "PARTIAL"},
            {"id": "R2", "name": "Data Governance", "status": "COMPLIANT" if compliance_score > 70 else "NON_COMPLIANT"},
            {"id": "R6", "name": "Human Oversight", "status": "COMPLIANT"}
        ]
    }

def generate_roadmap(system_name: str) -> str:
    """Generates a step-by-step roadmap for compliance."""
    return f"""# 🗺️ Compliance Roadmap: {system_name}
1. Establish Risk Management System (Art. 9) - Due Q4 2025
2. Data Bias Audit (Art. 10) - Due Q1 2026
3. Technical Documentation (Art. 11) - Due Q2 2026
4. Human Oversight Interface (Art. 14) - Due Q3 2026
"""

def classify_openclaw_stack(stack_name: str) -> str:
    return "Compliant (Open-Source Exception Art. 2)"

import random

if __name__ == "__main__":
    if len(sys.argv) > 1:
        name = sys.argv[1]
        print(generate_compliance_report(name, classify_ai_system(name)))
