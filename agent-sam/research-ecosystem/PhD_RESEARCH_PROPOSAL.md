# Multi-Agent AI Systems for Cancer Research: A Computational Oncology Framework

## PhD Research Proposal — Prime-AI (EURL)
### Principal Investigator: Yacine Benhamou
### Affiliation: Prime-AI (EURL) — Conflans-Sainte-Honorine, France
### Website: [prime-ai.fr](https://prime-ai.fr) | [yace19ai.com](https://yace19ai.com)
### Date: February 21, 2026

---

## Executive Summary

This proposal presents PRISM-Onco (Prime Research Intelligence System for Multi-Agent Oncology), a revolutionary multi-agent AI framework that leverages autonomous agent orchestration to accelerate cancer drug discovery, biomarker identification, and personalized treatment optimization. Building on Prime-AI's proven expertise in multi-agent system architecture (21 production systems, A2A/MCP protocol integration), this research bridges the gap between cutting-edge agentic AI and computational oncology — creating a self-driving research ecosystem capable of hypothesis generation, multi-omics data integration, and autonomous grant application.

The proposed framework addresses three critical challenges in modern cancer research:

1. **Data Integration Complexity**: Cancer biology generates terabytes of heterogeneous multi-omics data (genomic, transcriptomic, proteomic, metabolomic) that overwhelms traditional single-model AI approaches
2. **Research Velocity**: The average drug development cycle (12-15 years) is incompatible with the urgency of patient needs — multi-agent systems can compress this by 10x through parallel autonomous exploration
3. **Mechanism Understanding**: Complex biotech mechanisms (signaling pathways, immune evasion, tumor microenvironment dynamics) require ensemble reasoning that no single AI model can achieve

**Requested Funding**: €2.4M over 36 months
**Target Grants**: EU Horizon Europe HORIZON-MISS-2026-02-CANCER-01, EIC Pathfinder Challenge, Cancer Grand Challenges, NCI ITCR, BPI France Deep Tech

---

## 1. Background & Motivation

### 1.1 The Founder's Journey — From AI Engineering to Cancer Research

Yacine Benhamou, founder and sole entrepreneur of Prime-AI (EURL), has spent his career at the intersection of artificial intelligence and real-world impact. Starting in 2018, Prime-AI evolved from a retail AI platform into a multi-industry AI powerhouse serving renewable energy, medical, aeronautical, and automotive sectors.

**Key technical achievements that position this proposal:**
- Architected 21+ production AI systems (verified GitHub portfolio)
- Designed multi-agent orchestration frameworks (AgentY, AgentCoderYBE, Sovereign Ecosystem)
- Built real-time A2A (Agent-to-Agent) + MCP (Model Context Protocol) gateway (Agent SAM)
- Developed autonomous voice cloning pipelines for multilingual applications
- Created crypto/blockchain infrastructure (PrimeCrypto)
- Built security & networking dashboards (NETWORKING)
- Pioneered Faith-based AI applications bridging spirituality and technology

This trajectory — from enterprise automation to deeply personal AI applications — naturally leads to the ultimate challenge: **using multi-agent AI to fight cancer**, a disease that affects 19.3 million people annually and claims 10 million lives each year.

### 1.2 The Case for Multi-Agent AI in Oncology

Traditional AI in cancer research follows a single-model paradigm: one neural network for image analysis, one for genomic variant calling, one for drug-target prediction. This siloed approach mirrors the fragmented nature of cancer research itself.

**The multi-agent paradigm shift**:
Instead of one model doing everything, we deploy a *fleet* of specialized agents — each an expert in its domain — that collaborate through structured protocols to produce emergent intelligence:

```
                    ┌──────────────────────────────────────────┐
                    │        PRISM-Onco Orchestrator           │
                    │   (Agent SAM Architecture — A2A + MCP)   │
                    └──────────┬────────────┬──────────────────┘
                               │            │
           ┌───────────────────┼────────────┼───────────────────┐
           ▼                   ▼            ▼                   ▼
    ┌──────────────┐  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │  Genomics    │  │  Proteomics  │ │  Literature  │ │  Drug Design │
    │  Analyst     │  │  Expert      │ │  Miner       │ │  Architect   │
    │  Agent       │  │  Agent       │ │  Agent       │ │  Agent       │
    └──────┬───────┘  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
           │                 │                │                │
           ▼                 ▼                ▼                ▼
    ┌──────────────┐  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │  Pathway     │  │  Clinical    │ │  Digital Twin│ │  Grant       │
    │  Mapper      │  │  Trial       │ │  Simulator   │ │  Writer      │
    │  Agent       │  │  Analyst     │ │  Agent       │ │  Agent       │
    └──────────────┘  └──────────────┘ └──────────────┘ └──────────────┘
```

---

## 2. Research Objectives

### Primary Objectives

**O1**: Design and implement PRISM-Onco, a multi-agent AI framework for autonomous cancer research, built on proven A2A + MCP protocols

**O2**: Develop 8 specialized cancer research agents that collaboratively analyze multi-omics data, generate hypotheses, and design therapeutic compounds

**O3**: Create a Virtual Human Twin (VHT) module for simulating cancer progression and treatment response at the cellular, tissue, and organ levels

**O4**: Build an autonomous grant discovery and application system that continuously scans funding opportunities and generates competitive proposals

**O5**: Demonstrate clinical utility through 3 case studies in breast cancer (HER2+), non-small cell lung cancer (EGFR-mutated), and pancreatic ductal adenocarcinoma

### Secondary Objectives

**O6**: Develop an SEO-optimized knowledge dissemination engine that publishes research findings in human-quality scientific prose

**O7**: Create open-source tools for the scientific community under EUPL license

**O8**: Establish Prime-AI as a European leader in agentic AI for precision oncology

---

## 3. Research Methodology

### 3.1 The PRISM-Onco Agent Fleet

Each agent is an autonomous entity with specialized capabilities, communicating through the A2A protocol and using MCP for tool execution:

#### Agent 1: 🧬 Genomics Analyst
- **Role**: Process and interpret whole-genome sequencing (WGS), whole-exome sequencing (WES), and RNA-seq data
- **Capabilities**: Variant calling (SNPs, indels, CNVs, SVs), mutation signature analysis, tumor mutational burden calculation, microsatellite instability detection
- **Key Tools**: DeepVariant integration, GATK pipelines, custom transformer models for variant effect prediction
- **Training Data**: TCGA (33 cancer types), ICGC, gnomAD, ClinVar

#### Agent 2: 🔬 Proteomics Expert
- **Role**: Analyze protein expression, post-translational modifications, and protein-protein interactions in cancer
- **Capabilities**: Mass spectrometry data interpretation, phosphoproteomics analysis, protein structure prediction (AlphaFold3 integration)
- **Key Focus**: Druggable target identification, resistance mutation mapping, neoantigen prediction

#### Agent 3: 📚 Literature Miner
- **Role**: Continuously scan and synthesize the cancer research literature
- **Capabilities**: PubMed/bioRxiv/medRxiv scraping (200+ papers/hour), citation network analysis, contradiction detection, knowledge graph construction
- **Output**: Real-time literature reviews, emerging trend reports, hypotheses from cross-domain connections

#### Agent 4: 💊 Drug Design Architect
- **Role**: Design and optimize therapeutic molecules targeting identified cancer vulnerabilities
- **Capabilities**: De novo molecule generation (diffusion models), ADMET prediction, binding affinity simulation, polypharmacology analysis
- **Key Innovation**: Multi-objective optimization across efficacy, selectivity, toxicity, and synthesizability

#### Agent 5: 🗺️ Pathway Mapper
- **Role**: Model cancer signaling pathways and their perturbations
- **Capabilities**: KEGG/Reactome integration, dynamic pathway simulation, synthetic lethality prediction, resistance mechanism modeling
- **Key Focus**: Identifying pathway convergence points for combination therapy design

#### Agent 6: 🏥 Clinical Trial Analyst
- **Role**: Analyze clinical trial data and design optimal trial protocols
- **Capabilities**: ClinicalTrials.gov integration, patient stratification, endpoint optimization, real-world evidence synthesis
- **Output**: Trial design recommendations, patient matching, outcome prediction

#### Agent 7: 🧪 Digital Twin Simulator
- **Role**: Create and run virtual patient simulations
- **Capabilities**: Agent-based cellular modeling, pharmacokinetic/pharmacodynamic simulation, immune system modeling, treatment response prediction
- **Key Innovation**: Multi-scale modeling from molecular to organ level, incorporating patient-specific omics data

#### Agent 8: 📝 Grant Writer & SEO Engine
- **Role**: Autonomously discover funding opportunities and generate competitive proposals
- **Capabilities**: Grant database scanning (EU Horizon, NCI, ARPA-H, EIC, BPI France), proposal generation, budget optimization, compliance checking, impact narrative construction
- **SEO Integration**: Semantic content generation for research visibility, backlink strategy, SERP optimization for prime-ai.fr

### 3.2 Agent Communication Architecture

Built on Prime-AI's proven Agent SAM infrastructure:

```javascript
// A2A Protocol — Agent Discovery & Task Routing
{
  "protocol": "a2a/1.0",
  "agents": [
    {
      "id": "genomics-analyst",
      "capabilities": ["variant-calling", "mutation-signature", "tmb-calculation"],
      "endpoint": "http://prism.prime-ai.fr/agents/genomics"
    },
    {
      "id": "drug-architect",
      "capabilities": ["molecule-generation", "admet-prediction", "binding-simulation"],
      "endpoint": "http://prism.prime-ai.fr/agents/drug-design"
    }
    // ... 8 agents total
  ]
}

// MCP Protocol — Tool Invocation
{
  "method": "tools/call",
  "params": {
    "name": "genomics.variant_call",
    "arguments": {
      "sample_id": "TCGA-BRCA-A7-A0DA",
      "ref_genome": "GRCh38",
      "caller": "deepvariant"
    }
  }
}
```

### 3.3 Virtual Human Twin (VHT) Module

Aligned with **Horizon Europe HORIZON-MISS-2026-02-CANCER-01** call:

The VHT module creates patient-specific digital replicas that simulate:

1. **Molecular Level**: Gene regulatory networks, protein interaction cascades, metabolic flux
2. **Cellular Level**: Cell cycle dynamics, apoptosis/necrosis pathways, immune cell interactions
3. **Tissue Level**: Tumor microenvironment modeling, angiogenesis, invasion/metastasis
4. **Organ Level**: Pharmacokinetics, organ toxicity prediction, systemic immune response

```
Patient Biopsy Data → Genomics Agent → Proteomics Agent → Pathway Mapper
        ↓                                                        ↓
    [Multi-omics                                          [Pathway Model]
     Profile]                                                    ↓
        └──────────────→ Digital Twin Simulator ←──────────────┘
                              ↓
                    [Virtual Patient Model]
                              ↓
                    Drug Design Architect
                              ↓
                    [Optimized Treatment Plan]
                              ↓
                    Clinical Trial Analyst
                              ↓
                    [Trial Design & Patient Matching]
```

### 3.4 Autonomous Grant Application Pipeline

The Grant Writer Agent continuously:

1. **Scans** funding databases (EU Funding Portal, grants.gov, ANRT France, BPI France)
2. **Matches** opportunities against PRISM-Onco capabilities and research outputs
3. **Generates** tailored proposals with proper formatting, budgets, timelines
4. **Reviews** using Literature Miner for supporting evidence
5. **Submits** (with human approval gate) to funding bodies

**Target grants for 2026-2027:**

| Grant | Body | Deadline | Budget | Fit |
|-------|------|----------|--------|-----|
| HORIZON-MISS-2026-02-CANCER-01 | EU Horizon Europe | Sep 15, 2026 | €6-10M | ★★★★★ — VHT for cancer |
| DIGITAL-2026-AI-09-SOLUTIONS-CANCER | EU Digital Europe | 2026 | €2-5M | ★★★★★ — AI imaging |
| EIC Pathfinder Challenge | EIC | Oct 2025 | €3-4M | ★★★★☆ — Gen-AI for cancer |
| Cancer Grand Challenges | CRUK | Rolling | £20M | ★★★★★ — Interdisciplinary AI |
| FDT-BioTech | NSF/NIH/FDA | Apr 10, 2026 | $1-2M | ★★★★☆ — Digital twins biotech |
| NCI ITCR | NIH/NCI | Multiple | $500K-2M | ★★★★☆ — Informatics cancer |
| ARPA-H Open | ARPA-H | Rolling | Variable | ★★★☆☆ — Transformative health |
| BPI France Deep Tech | BPI France | Rolling | €500K-3M | ★★★★★ — French deep tech |
| Biswas Foundation | Private | Annual | $1M | ★★★★☆ — Computational bio |
| Novo Nordisk / BII | Foundation | Rolling | Variable | ★★★☆☆ — Biotech startup |

---

## 4. Technical Innovation

### 4.1 Reinforcement Learning with Verifiable Rewards (RLVR) for Scientific Agents

Each PRISM-Onco agent is trained using RLVR:
- **Reward signals**: Experimentally verifiable outcomes (published results, known drug-target pairs, validated biomarkers)
- **Verification loop**: Agent generates hypothesis → Literature Miner checks against known science → Digital Twin simulates → Clinical Analyst validates feasibility
- **Self-correction**: Agents learn from failed hypotheses, building adversarial robustness

### 4.2 Semantic SEO Knowledge Engine

The Grant Writer/SEO agent produces:
- **Research blog posts** optimized for cancer research keywords (E-E-A-T compliant)
- **Technical white papers** with proper schema.org markup for Google Scholar
- **Social proof content** linking prime-ai.fr to high-authority cancer research domains
- **Multilingual content** (French, English, Arabic) leveraging Prime-AI's voice cloning and translation capabilities

SEO Strategy pillars:
1. **Topical Authority**: 50+ deep-dive articles on AI in oncology, published on prime-ai.fr/research
2. **Backlink Acquisition**: Contribution to open-source cancer research tools → natural backlinks from university domains
3. **Technical SEO**: JSON-LD structured data for research publications, author schema, organization schema
4. **Content Velocity**: 3-5 research articles per week, autonomously generated by the Literature Miner + Grant Writer agents

### 4.3 EU AI Act Compliance (Leveraging Existing Infrastructure)

Building on Prime-AI's existing EU AI Act compliance server (eu_ai_act_server.py), PRISM-Onco is designed as a **high-risk AI system** (Article 6, Annex III) and implements:
- Full transparency documentation
- Human oversight mechanisms (all agent decisions logged and reviewable)
- Data governance (GDPR-compliant patient data handling)
- Robustness testing (adversarial evaluation of agent outputs)

---

## 5. Timeline & Milestones

### Year 1 (Months 1-12): Foundation & First Agents
| Month | Milestone | Deliverable |
|-------|-----------|-------------|
| 1-3 | Infrastructure | A2A/MCP orchestrator deployed (Agent SAM v2.0) |
| 3-6 | Agent Development | Genomics Analyst + Literature Miner agents operational |
| 6-9 | Integration | Multi-agent data pipeline for TCGA breast cancer dataset |
| 9-12 | First Results | Published analysis of HER2+ breast cancer genomic landscape |

### Year 2 (Months 13-24): Expansion & VHT
| Month | Milestone | Deliverable |
|-------|-----------|-------------|
| 13-15 | Agent Fleet | All 8 agents operational |
| 15-18 | VHT Module | Virtual Human Twin v1.0 for breast cancer |
| 18-21 | Drug Design | 5 novel compound candidates for HER2+ resistance |
| 21-24 | Clinical Validation | Retrospective validation against real clinical outcomes |

### Year 3 (Months 25-36): Scale & Impact
| Month | Milestone | Deliverable |
|-------|-----------|-------------|
| 25-28 | Multi-cancer | Extension to NSCLC and pancreatic cancer |
| 28-32 | Autonomous Grants | 10+ autonomous grant applications submitted |
| 32-34 | Open Source | PRISM-Onco core released under EUPL |
| 34-36 | Commercialization | SaaS platform for research institutions |

---

## 6. Budget

### Total Request: €2,400,000 over 36 months

| Category | Year 1 | Year 2 | Year 3 | Total |
|----------|--------|--------|--------|-------|
| Personnel (PI + 2 postdocs + 1 engineer) | €350,000 | €400,000 | €420,000 | €1,170,000 |
| Compute (GPU clusters, cloud) | €150,000 | €200,000 | €150,000 | €500,000 |
| Data & Licenses (TCGA, PDB, literature) | €50,000 | €40,000 | €30,000 | €120,000 |
| Equipment & Infrastructure | €100,000 | €50,000 | €30,000 | €180,000 |
| Travel & Conferences | €30,000 | €40,000 | €50,000 | €120,000 |
| Open Source Development | €40,000 | €50,000 | €60,000 | €150,000 |
| Administrative & Legal | €30,000 | €30,000 | €30,000 | €90,000 |
| Contingency (3%) | €24,000 | €24,000 | €22,000 | €70,000 |
| **Total** | **€774,000** | **€834,000** | **€792,000** | **€2,400,000** |

---

## 7. Impact & Societal Relevance

### Scientific Impact
- First multi-agent AI framework purpose-built for autonomous cancer research
- Novel RLVR methodology for training scientific reasoning agents
- Virtual Human Twin models advancing personalized oncology

### Economic Impact
- Prime-AI positions France as a leader in agentic AI for healthcare
- SaaS platform creates sustainable revenue for further research
- Reduces drug development costs by targeting only high-probability candidates

### Societal Impact
- Accelerates access to precision cancer treatments for underserved populations
- Open-source tools democratize AI-powered cancer research
- EU AI Act-compliant framework serves as a model for responsible AI in healthcare

### Alignment with EU Mission on Cancer
- Directly targets the EU goal of improving lives of 3+ million people by 2030
- Contributes to prevention (biomarker identification), cure (drug design), and quality of life (personalized treatment)

---

## 8. Competitive Advantage

### Why Prime-AI?

| Factor | Prime-AI (PRISM-Onco) | Traditional Approaches |
|--------|----------------------|----------------------|
| Agent architecture | 8 specialized, collaborating agents | Single monolithic model |
| Protocol standard | A2A + MCP (industry standard) | Proprietary APIs |
| Data integration | Multi-omics + literature + clinical | Usually single data type |
| Autonomy | Self-directed research & grant application | Human-in-the-loop only |
| EU compliance | Built-in (EU AI Act, GDPR) | Often retrofitted |
| Open source | EUPL license | Usually proprietary |
| Multilingual | French, English, Arabic SEO content | English only |
| Founder expertise | 21 production AI systems, 8+ years | Academic only (typically) |

---

## 9. References

1. Topol, E.J. "High-performance medicine: the convergence of human and artificial intelligence." *Nature Medicine* 25, 44–56 (2019).
2. Wang, G. et al. "Multi-Agent AI for Autonomous Scientific Discovery." *Nature Reviews Drug Discovery* (2026).
3. EU Commission. "Horizon Europe Work Programme 2025-2027: Health." European Commission (2025).
4. PharmaMar & Globant. "Multi-Agent AI Achieves 90% Accuracy in Oncology Data Retrieval." Press Release (2026).
5. Manchester University. "Agentic AI for Integrative Multi-Omics Research in Cancer." PhD Opening (2026).
6. European Innovation Council. "EIC Pathfinder Challenge: Generative AI for Cancer Diagnosis." (2025).
7. NSF/NIH/FDA. "Foundations for Digital Twins as Catalyzers of Biomedical Innovation (FDT-BioTech)." (2026).
8. Cancer Grand Challenges. "AI Agents for Cancer Hypothesis Generation." (2026).
9. ARPA-H. "Transformative Research for Accelerating Cures." (2026).
10. BPI France. "Deep Tech Grants Program." (2026).

---

## 10. Appendix: Technical Specifications

### A. System Architecture (Deployed)

```
Prime-AI Infrastructure (Already Built):
├── Agent SAM Gateway (Node.js) — A2A v1.0 + MCP v1.0
│   ├── ChamberManager (process isolation)
│   ├── A2A Server (discovery, task routing)
│   ├── MCP Bridge (tool invocation)
│   └── TaskRouter (intelligent routing)
├── OpenClaw Chamber (messaging, automation)
├── Agent Zero Chamber (coding, research)
├── PicoClaw Chamber (lightweight AI)
└── SAM CLI (command interface)

PRISM-Onco Extension (Proposed):
├── GenomicsAgent (DeepVariant, GATK, custom transformers)
├── ProteomicsAgent (AlphaFold3, mass spec analysis)
├── LiteratureMiner (PubMed API, graph DB, transformer models)
├── DrugArchitect (diffusion models, docking simulation)
├── PathwayMapper (KEGG/Reactome, dynamic simulation)
├── ClinicalAnalyst (ClinicalTrials.gov, outcome prediction)
├── DigitalTwinSimulator (agent-based modeling, PK/PD)
└── GrantWriter (EU Portal, SEO engine, proposal generation)
```

### B. Key Performance Indicators

| KPI | Year 1 | Year 2 | Year 3 |
|-----|--------|--------|--------|
| Agents operational | 3 | 8 | 8+ |
| Hypotheses generated | 100 | 1,000 | 5,000 |
| Papers published | 2 | 5 | 10 |
| Grant applications | 3 | 10 | 20 |
| Novel drug candidates | 0 | 5 | 15 |
| VHT patients simulated | 0 | 100 | 1,000 |
| prime-ai.fr monthly traffic | 5K | 25K | 100K |
| SERP rankings (AI oncology) | Top 50 | Top 20 | Top 5 |

---

*Submitted by Yacine Benhamou, Founder & CEO*
*Prime-AI (EURL) — 5 Rue Eugene Freyssinet, 78700 Conflans-Sainte-Honorine, France*
*SIREN: 990 020 893*
*Contact: yacine@prime-ai.fr*
*Web: prime-ai.fr | yace19ai.com*
