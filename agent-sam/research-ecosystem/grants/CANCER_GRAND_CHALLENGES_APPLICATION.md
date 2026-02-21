# Cancer Grand Challenges — Full Application
## CRUK + NCI Joint Programme
### Team: "PRISM" — Precision Research through Intelligent Systems of Multi-agents

---

## Challenge Area: Digital and computational approaches to understand cancer

---

## 1. Executive Summary

Cancer research faces a paradox: we generate more molecular data than ever, yet translating this into effective therapies remains agonizingly slow. The bottleneck is no longer data generation — it is data integration and hypothesis generation across modalities.

**PRISM** proposes a radically new approach: autonomous multi-agent AI systems that conduct cancer research at machine speed. Our system, PRISM-Onco, orchestrates 8 specialized AI agents that collaborate to perform end-to-end oncology research — from genomic analysis through drug design to treatment response prediction — in hours rather than years.

This is not another AI tool for researchers to use. This is an AI research team that operates autonomously, generating and testing hypotheses across genomic, proteomic, pharmacological, and clinical domains simultaneously.

**Budget requested: £20,000,000 over 5 years**
**Countries involved: France, Germany, Netherlands, UK, USA**

---

## 2. The Challenge We Address

### 2.1 The Integration Crisis
Modern oncology generates multi-modal data at unprecedented scale:
- 3 billion base pairs per whole genome sequence
- 20,000+ protein expression measurements per tumor
- 35+ million articles in PubMed
- 400,000+ clinical trials registered globally
- 12,000+ approved and investigational drugs

No human researcher — or team of researchers — can integrate across all these modalities simultaneously. Yet the most impactful discoveries occur at the intersections between domains.

### 2.2 Why Current AI Falls Short
Existing AI approaches in oncology are **single-task and siloed**:
- AlphaFold predicts protein structures but doesn't connect to clinical outcomes
- Foundation models analyze genomics but don't design drugs
- Literature mining tools extract facts but don't generate hypotheses

**What's missing: a system that reasons across ALL modalities simultaneously.**

### 2.3 Our Solution: Collaborative AI Agents
PRISM-Onco deploys 8 specialized agents that communicate via standardized protocols (A2A, MCP), enabling:
- **Cross-modal reasoning**: The genomics agent identifies a mutation → the pathway agent maps its functional impact → the drug agent designs a targeted inhibitor → the digital twin predicts patient response
- **Emergent discovery**: Interactions between agents surface hypotheses invisible to any single agent
- **Scalable research**: The system processes 200+ papers/hour, analyzes thousands of variants, and screens millions of compound combinations

---

## 3. Research Programme

### Phase 1: Architecture & Validation (Years 1-2) — £7M

**WP1: Multi-Agent Platform Engineering** (Lead: Prime.AI)
- Build production-grade PRISM-Onco platform
- Implement A2A/MCP communication protocols
- Develop SAM (Sovereign Agent Manager) orchestrator
- Create agent training pipelines for 8 specialized domains
- Milestone: Platform operational with all 8 agents (M12)

**WP2: Retrospective Clinical Validation** (Lead: DKFZ)
- Validate against 5 cancer types using TCGA + institutional cohorts:
  1. HER2+ Breast Cancer (n=500)
  2. EGFR-mutant NSCLC (n=400)
  3. Pancreatic Ductal Adenocarcinoma (n=300)
  4. Colorectal Cancer (MSI-H vs MSS) (n=600)
  5. Glioblastoma Multiforme (n=250)
- Compare PRISM-Onco recommendations vs actual tumor board decisions
- Metric: ≥85% concordance with expert clinical decisions
- Milestone: Validation report for 5 cancers (M24)

### Phase 2: Discovery & Translation (Years 3-4) — £8M

**WP3: Novel Target Discovery** (Lead: NKI + CNIO)
- Deploy PRISM-Onco for autonomous target discovery
- Focus: identify synthetic lethality pairs unreported in literature
- Experimental validation of top agent-generated hypotheses in wet lab
- Target: 10+ novel druggable targets validated in vitro
- Milestone: 3+ targets advancing to hit identification (M36)

**WP4: AI-Driven Drug Design** (Lead: Prime.AI + Academic Partner)
- Generative drug design using PRISM-Onco's Drug Architect agent
- ADMET prediction and optimization
- In silico clinical trial simulation via Digital Twin agent
- Target: 5+ lead compounds with IC50 < 10 nM
- Milestone: 2+ compounds entering preclinical evaluation (M48)

**WP5: Clinical Integration Pilot** (Lead: Gustave Roussy)
- Prospective advisory integration in molecular tumor board
- Non-interventional: PRISM-Onco provides recommendations, clinicians decide
- Evaluate added value: novel options identified, time saved, clinician satisfaction
- n=100 patients across 3 cancer types
- Milestone: Clinical utility assessment report (M48)

### Phase 3: Scaling & Legacy (Year 5) — £5M

**WP6: Platform Scaling & Open Science** (Lead: All Partners)
- Scale to 15+ cancer types
- Open-source core platform release
- Training programme for 20+ research institutions
- Policy recommendations for AI-augmented clinical research
- Sustainability plan: SaaS licensing model

**WP7: Education & Outreach** (Lead: All)
- PhD programmes (5 doctoral students across consortium)
- Summer school: "AI Agents for Biomedical Research"
- Public engagement: documentary/podcast on AI in cancer research
- Patient advocacy group collaboration

---

## 4. Team

### Prime.AI (France) — AI Architecture & Orchestration
- **Yacine Benhamou**, Lead AI Builder — 21 multi-agent systems in production
- Expertise: Agentic AI, A2A/MCP protocols, multi-system orchestration
- Role: Platform development, agent architecture, coordination

### DKFZ — German Cancer Research Center (Germany) — Bioinformatics
- **[PI TBD]**, Division of Applied Bioinformatics
- Expertise: Cancer genomics, computational oncology, TCGA analysis
- Role: Genomic validation, data integration, WP2 lead

### NKI — Netherlands Cancer Institute (Netherlands) — Translational Research
- **[PI TBD]**, Division of Molecular Oncology
- Expertise: Functional genomics, synthetic lethality screens
- Role: Target discovery, experimental validation, WP3 co-lead

### Gustave Roussy (France) — Clinical Oncology
- **[PI TBD]**, Department of Medical Oncology
- Expertise: Molecular tumor boards, precision oncology, basket trials
- Role: Clinical validation, prospective pilot, WP5 lead

### MD Anderson / Memorial Sloan Kettering (USA) — Clinical AI
- **[PI TBD]**, Department of Genomic Medicine / Computational Oncology
- Expertise: Clinical AI deployment, large-scale genomic studies
- Role: US clinical validation, regulatory framework, data sharing

### CNIO — Spanish National Cancer Research Centre (Spain) — Drug Design
- **[PI TBD]**, Structural Biology & Drug Discovery
- Expertise: Computational chemistry, target validation, drug design
- Role: Drug design validation, WP4 co-lead

---

## 5. Budget

| Partner | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 | Total |
|---------|--------|--------|--------|--------|--------|-------|
| Prime.AI | £800K | £800K | £700K | £600K | £500K | £3,400K |
| DKFZ | £700K | £700K | £600K | £500K | £400K | £2,900K |
| NKI | £500K | £600K | £800K | £700K | £400K | £3,000K |
| Gustave Roussy | £400K | £500K | £700K | £800K | £500K | £2,900K |
| MD Anderson/MSK | £600K | £600K | £800K | £700K | £500K | £3,200K |
| CNIO | £400K | £500K | £700K | £700K | £300K | £2,600K |
| Management & Contingency | £200K | £300K | £400K | £500K | £600K | £2,000K |
| **Total** | **£3,600K** | **£4,000K** | **£4,700K** | **£4,500K** | **£3,200K** | **£20,000K** |

### Budget Categories
| Category | Amount | % |
|----------|--------|---|
| Personnel (researchers, postdocs, PhD students) | £10,000K | 50% |
| Equipment & Cloud computing | £3,000K | 15% |
| Consumables & Lab supplies | £2,000K | 10% |
| Travel & Conferences | £1,000K | 5% |
| Subcontracting | £1,500K | 7.5% |
| Management & Overhead | £2,500K | 12.5% |
| **Total** | **£20,000K** | **100%** |

---

## 6. Expected Outputs

| Output | Timeline | Impact |
|--------|----------|--------|
| PRISM-Onco open-source platform | M18 | Global research community access |
| 5-cancer validation benchmark | M24 | New standard for AI in oncology |
| 10+ novel druggable targets | M36 | New therapeutic opportunities |
| 5+ lead drug compounds | M48 | Preclinical pipeline |
| Clinical utility evidence (n=100) | M48 | Regulatory pathway evidence |
| 15-20 publications | M12-M60 | Scientific impact |
| 5 PhD graduates | M60 | Workforce development |
| AI training programme for 20+ institutions | M48-M60 | Capacity building |
| Policy framework for AI in clinical research | M48 | Regulatory guidance |

---

## 7. Why This Team?

This is the **only team in the world** that combines:
1. **Operational multi-agent AI expertise** (Prime.AI — 21 systems deployed)
2. **Top-tier cancer research** (DKFZ, NKI, Gustave Roussy, MD Anderson)
3. **Structural biology & drug design** (CNIO)
4. **Cross-continental reach** (France, Germany, Netherlands, Spain, USA)

No other group has built and deployed production-grade multi-agent systems AND has access to the clinical datasets needed for validation.

---

## 8. Submission Information

| Field | Value |
|-------|-------|
| **Programme** | Cancer Grand Challenges |
| **Funders** | Cancer Research UK (CRUK) + National Cancer Institute (NCI) |
| **Award** | Up to £20M over 5 years |
| **Application** | Two-stage: Expression of Interest → Full Application |
| **Website** | https://cancergrandchallenges.org |
| **Contact** | challenges@cancer.org.uk |

### Submission Checklist
- [ ] Expression of Interest (2-page summary)
- [ ] Full Application (if invited — 15-page proposal)
- [ ] Team CVs (2 pages each)
- [ ] Letters of institutional support from all partners
- [ ] Budget justification
- [ ] Data management plan
- [ ] Ethics statement
