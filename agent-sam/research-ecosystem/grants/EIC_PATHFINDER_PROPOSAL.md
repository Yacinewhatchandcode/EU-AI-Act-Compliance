# EIC Pathfinder Open — Full Proposal
## European Innovation Council — Pathfinder Open 2026
### "Generative AI Multi-Agent Systems for Autonomous Cancer Research"

---

## PART B — Technical Annex

### Section 1: Excellence

#### 1.1 Long-Term Vision

We envision a future where cancer research operates at machine speed — where autonomous AI agents collaborate to generate, test, and refine therapeutic hypotheses faster than any human team. PRISM-Onco represents the first step toward this vision: a multi-agent system where 8 specialized AI agents, each powered by a large language model (LLM), autonomously conduct end-to-end oncology research.

This is not incremental improvement. It is a fundamental paradigm shift from **human-directed AI tools** to **AI-directed research pipelines**, where human researchers set the objective and the multi-agent system autonomously designs and executes the research plan.

#### 1.2 Breakthrough S&T Objectives

**Objective 1: Emergent Scientific Discovery via Multi-Agent Collaboration**
Demonstrate that a system of 8+ specialized LLM-based agents can generate novel therapeutic hypotheses that no single agent — or conventional computational pipeline — can produce. We define "emergent discovery" as an actionable research finding that:
- Was not present in any single agent's training data or tools
- Arose only from the interaction between 2+ agents
- Can be experimentally validated

**Objective 2: Formal Framework for Biomedical Multi-Agent Systems**
Develop a mathematically rigorous framework for multi-agent reasoning in biomedicine, including:
- Bayesian consensus protocols for aggregating agent recommendations
- Conflict resolution mechanisms when agents disagree
- Provenance tracking for scientific claims across the agent chain
- Uncertainty quantification for downstream therapeutic recommendations

**Objective 3: Autonomous Research Pipeline Validation**
Validate the PRISM-Onco pipeline on 5 cancer types with retrospective clinical data, demonstrating:
- ≥85% concordance with tumor board decisions
- Identification of ≥3 novel druggable targets per cancer type
- Drug candidates with predicted IC50 < 10 nM
- Digital twin prediction accuracy ≥75% (treatment response)

#### 1.3 Novelty and Foundational Nature

| Aspect | State-of-the-Art | PRISM-Onco Breakthrough |
|--------|------------------|------------------------|
| AI in oncology | Single-task models (AlphaFold, DeepVariant) | Multi-agent orchestration across 8 domains |
| Drug discovery | Sequential pipelines (target → hit → lead → optimize) | Parallel multi-agent exploration with cross-validation |
| Literature mining | Keyword search / single-model extraction | Agent-driven knowledge graph construction with >200 papers/hour |
| Digital twins | Compartmental PK/PD models | LLM-augmented physiological simulation with real-time adaptation |
| Agent architecttic | ReAct / Chain-of-Thought single agent | 8-agent A2A/MCP orchestration with emergent reasoning |

#### 1.4 Interdisciplinarity and Methodology

**Research Methodology:**

1. **Agent Architecture Design** (M1-M12): Formal specification of each agent's capabilities, communication protocols, and knowledge boundaries using the A2A (Google) and MCP (Anthropic) standards.

2. **Orchestration Engine** (M6-M18): Development of the SAM (Sovereign Agent Manager) orchestrator with:
   - Dynamic task allocation based on agent competency profiles
   - Bayesian belief aggregation across heterogeneous agent outputs
   - Adversarial validation (agents challenge each other's findings)

3. **Domain Agent Training** (M6-M24): Fine-tuning of specialized LLMs for each of the 8 domains using domain-specific corpora (PubMed, TCGA, ChEMBL, ClinicalTrials.gov, UniProt, STRING, DrugBank).

4. **Retrospective Validation** (M18-M36): Comparison against historical tumor board decisions from clinical partners across 5 cancer types.

5. **Prospective Pilot** (M30-M42): Real-time integration with one clinical partner for advisory recommendations (non-interventional).

---

### Section 2: Impact

#### 2.1 Pathways to Impact

**Scientific Impact:**
- 8-12 publications in top-tier journals (Nature Methods, Nature Cancer, Cell Systems, Bioinformatics, JMLR, NeurIPS)
- Open-source framework for biomedical multi-agent systems
- New benchmark datasets for evaluating AI-driven cancer research

**Economic Impact:**
- €50M+ potential licensing revenue by Year 5 post-project
- 3-5 spin-off opportunities (per-cancer-type platforms)
- 150+ high-skilled jobs (AI + biotech intersection)

**Societal Impact:**
- Democratization of cutting-edge cancer research capabilities
- Accelerated drug discovery timeline: 10 years → 3-5 years
- Precision medicine accessible to smaller research institutions

#### 2.2 Measures to Maximise Impact

| Activity | Timeline | KPI |
|----------|----------|-----|
| Open-source PRISM-Onco core | M18 | 500+ GitHub stars, 50+ forks |
| Preprint publications | M12, M24, M36 | 8+ papers |
| International conferences | Yearly | NeurIPS, MICCAI, AACR, ASCO |
| Patent filings | M24, M36 | 2-3 patents |
| Industry partnerships | M24+ | 3+ pharma company LOIs |
| Clinical validation paper | M36 | 1 high-impact validation study |

#### 2.3 Open Science Practices

- All publications available as preprints (bioRxiv/arXiv)
- Core framework released under Apache 2.0 license
- Datasets deposited in Zenodo with DOI
- Reproducibility packages for all experiments
- FAIR data management plan

---

### Section 3: Implementation

#### 3.1 Work Plan

**WP1: Multi-Agent Architecture (M1-M18) — Lead: Prime.AI**
- T1.1: Agent specification and protocol design (M1-M6)
- T1.2: A2A/MCP communication layer implementation (M4-M12)
- T1.3: SAM orchestrator development (M6-M18)
- D1.1: Architecture specification document (M6)
- D1.2: Working prototype with 8 agents (M18)

**WP2: Domain Agent Development (M6-M30) — Lead: Academic Partner 1**
- T2.1: Genomics + Proteomics agents (M6-M18)
- T2.2: Literature + Drug Design agents (M12-M24)
- T2.3: Clinical + Digital Twin agents (M18-M30)
- D2.1: Trained domain agents with benchmarks (M24)
- D2.2: Integrated pipeline validation (M30)

**WP3: Clinical Validation (M18-M42) — Lead: Clinical Partner**
- T3.1: Retrospective validation on 5 cancer types (M18-M36)
- T3.2: Prospective pilot study design (M30-M36)
- T3.3: Prospective pilot execution (M36-M42)
- D3.1: Validation report (M36)
- D3.2: Pilot study report (M42)

**WP4: Dissemination & Exploitation (M1-M48) — Lead: Prime.AI**
- T4.1: Publications and conferences
- T4.2: Open-source releases
- T4.3: Patent filings and exploitation strategy
- T4.4: Commercialization roadmap
- D4.1: Exploitation plan (M12, updated M36)

**WP5: Project Management (M1-M48) — Lead: Prime.AI**
- T5.1: Coordination and reporting
- T5.2: Risk management
- T5.3: Ethics and data management

#### 3.2 Consortium

**Partner 1: Prime.AI (France) — Coordinator**
- Role: Architecture, orchestration, WP1 lead, WP4-5 lead
- Key person: Yacine Benhamou (Lead AI Builder, 21 multi-agent systems)
- Contribution: €1.2M (30 PM)

**Partner 2: [Academic AI Lab — e.g., MILA / INRIA / TU Munich]**
- Role: Agent training, formal methods, WP2 lead
- Key person: [Prof. TBD]
- Contribution: €1.0M (36 PM)

**Partner 3: [Cancer Research Institute — e.g., Gustave Roussy / DKFZ / NKI]**
- Role: Clinical data, validation, WP3 lead
- Key person: [Prof. TBD]
- Contribution: €1.0M (24 PM)

**Partner 4: [Computational Biology Lab — e.g., EMBL-EBI / SIB / CNIO]**
- Role: Bioinformatics pipelines, data integration
- Key person: [Prof. TBD]
- Contribution: €0.8M (24 PM)

#### 3.3 Budget Summary

| Partner | Personnel | Equipment | Travel | Subcontracting | Other | Total |
|---------|-----------|-----------|--------|----------------|-------|-------|
| Prime.AI | 720K | 180K | 60K | 120K | 120K | 1,200K |
| Partner 2 | 600K | 200K | 50K | 50K | 100K | 1,000K |
| Partner 3 | 650K | 100K | 60K | 100K | 90K | 1,000K |
| Partner 4 | 500K | 150K | 40K | 50K | 60K | 800K |
| **Total** | **2,470K** | **630K** | **210K** | **320K** | **370K** | **4,000K** |

#### 3.4 Risk Management

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| LLM hallucinations in medical context | High | Critical | Multi-agent cross-validation + human-in-the-loop for clinical recommendations |
| Insufficient clinical data access | Medium | High | Multiple clinical partners + public datasets (TCGA, GDC) |
| Agent convergence failure | Medium | Medium | Bayesian consensus with fallback to majority voting |
| Regulatory/ethical barriers | Low | High | Ethics board review + GDPR compliance by design |
| Partner withdrawal | Low | High | Minimum 4 partners, tasks redistributable |

---

### Section 4: Ethics & Data Management

#### 4.1 Ethical Considerations
- All patient data fully anonymized (GDPR Article 9 compliant)
- No interventional clinical decisions made by the system
- AI recommendations always advisory, never prescriptive
- Ethics committee approval obtained before any clinical data access
- Algorithmic fairness: bias auditing across demographic groups

#### 4.2 Data Management Plan
- Data stored in EU-sovereign cloud infrastructure
- FAIR principles applied to all generated datasets
- Code versioned on GitHub with DOI via Zenodo
- Publications deposited in institutional repositories

---

## Administrative Data

| Field | Value |
|-------|-------|
| **Call** | EIC-2026-PATHFINDEROPEN |
| **Programme** | Horizon Europe — European Innovation Council |
| **Funding scheme** | EIC Pathfinder Open |
| **Duration** | 48 months |
| **Total budget** | €4,000,000 |
| **EU contribution** | €4,000,000 (100%) |
| **Coordinator** | PRIME.AI (France) |
| **Number of partners** | 4 (minimum 3 EU countries) |
| **TRL start** | TRL 2 |
| **TRL end** | TRL 4 |

---

## Submission Checklist

- [ ] EU Funding Portal account (all partners)
- [ ] PIC number for each partner
- [ ] Part A: Administrative forms (online)
- [ ] Part B: This document (PDF upload, max 17 pages)
- [ ] Ethics self-assessment
- [ ] Budget details (online form)
- [ ] Letters of commitment from all partners
- [ ] CV of key researchers (max 2 pages each)
