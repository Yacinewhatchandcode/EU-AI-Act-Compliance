# NSF Convergence Accelerator — Digital Twins for Biotech
## Track: Digital Twins for Living Systems
### NSF Program: NSF 26-XXX (anticipated FY2026)

---

## Project Title
**PRISM-Onco: Multi-Agent AI Digital Twins for Precision Cancer Treatment Optimization**

---

## 1. Project Summary (1 page)

### Overview
Cancer treatment decisions involve integrating vast molecular, clinical, and pharmacological data — a task that exceeds human cognitive capacity. We propose PRISM-Onco, a revolutionary multi-agent AI system that creates comprehensive digital twins of cancer patients by orchestrating 8 specialized AI agents. Each agent models a different biological dimension (genomics, proteomics, drug pharmacology, immune response, etc.), and their collaboration produces an integrated patient digital twin capable of predicting treatment response before drug administration.

### Intellectual Merit
This project advances the science of digital twins by demonstrating that multi-agent AI systems can create more accurate and comprehensive patient models than any single computational approach. Our key innovations include: (1) a formal framework for multi-agent digital twin construction, (2) Bayesian consensus protocols for integrating heterogeneous biological models, and (3) the first validation of LLM-based digital twins against clinical treatment outcomes in oncology.

### Broader Impacts
PRISM-Onco will democratize precision oncology by providing research institutions and community oncologists with AI-powered treatment optimization tools. The open-source platform will enable any institution to deploy multi-agent digital twins, reducing the expertise gap between academic medical centers and community practices. We will train 10+ researchers in multi-agent AI for biomedicine and develop curriculum modules for graduate education.

### Keywords
Digital twin, multi-agent systems, precision oncology, large language models, drug response prediction, A2A protocol, MCP protocol

---

## 2. Project Description (15 pages max)

### 2.1 Introduction and Motivation

Precision oncology promises to match each patient with the optimal therapy based on their tumor's molecular profile. Despite advances in genomic profiling (OncoKB, FoundationOne), treatment selection still relies heavily on clinician experience and population-level evidence. A recent study found that only 7% of cancer patients receive genomically-matched therapy (Marquart et al., 2020).

The core challenge is **integration**: no single model can capture the full complexity of a patient's disease. Genomic data alone misses post-translational modifications; proteomic data misses clonal evolution; clinical trial data misses individual pharmacokinetics. A true digital twin must integrate ALL these dimensions.

**Our hypothesis: A system of collaborating specialized AI agents can construct more accurate and actionable patient digital twins than any monolithic model.**

### 2.2 PRISM-Onco Architecture

PRISM-Onco is built on the Agent-to-Agent (A2A) protocol developed by Google DeepMind and the Model Context Protocol (MCP) by Anthropic. These industrial standards enable reliable communication between autonomous AI agents.

**The 8 Agents:**

| Agent | Domain | Digital Twin Component |
|-------|--------|----------------------|
| Genomics Analyst | Variant calling, TMB, MSI, CNV | Mutational landscape model |
| Proteomics Expert | Druggable targets, protein structure | Target accessibility model |
| Literature Miner | PubMed, knowledge graphs | Evidence integration layer |
| Drug Architect | Molecule design, ADMET | Pharmacological model |
| Pathway Mapper | Signaling cascades, synthetic lethality | Pathway activity model |
| Clinical Analyst | Trial matching, stratification | Population reference model |
| Digital Twin Core | PK/PD, immune simulation | Patient physiology model |
| Scientific Writer | Report generation, regulatory docs | Output synthesis |

**Orchestration via SAM (Sovereign Agent Manager):**
The SAM orchestrator coordinates agent workflows, manages data dependencies, resolves conflicts via Bayesian consensus, and produces the integrated digital twin output.

### 2.3 Research Plan

**Phase 1 (Year 1): Foundation — $600K**
- Develop and validate the multi-agent digital twin architecture
- Implement A2A/MCP communication layer for 8 agents
- Construct digital twins for 100 TCGA patients (breast, lung, pancreatic cancer)
- Benchmark against ground truth treatment outcomes
- Deliverable: Working prototype with validation on 3 cancer types

**Phase 2 (Year 2): Validation & Extension — $700K**
- Extend to 1,000 patients across 5 cancer types
- Partner with [US Clinical Site] for access to additional clinical cohorts
- Improve digital twin accuracy using feedback loops
- Develop uncertainty quantification framework
- Deliverable: Validated platform with ≥75% treatment response prediction accuracy

**Phase 3 (Year 3): Translation — $700K**
- Prospective pilot at [US Clinical Site]: real-time digital twin generation for molecular tumor board
- Develop user interface for clinical integration
- Open-source platform release
- Sustainability plan (SaaS model for commercial use)
- Deliverable: Clinical-ready platform, user study results, sustainability plan

### 2.4 Evaluation Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Treatment response prediction accuracy | ≥75% | Concordance with actual patient outcomes |
| Novel actionable recommendations | ≥30% | Recommendations not in standard guidelines |
| Time to digital twin generation | < 4 hours | Wall-clock time from data input to recommendation |
| Agent consensus reliability | ≥90% | Agreement across multiple independent runs |
| Clinician acceptance rate | ≥70% | Survey of molecular tumor board participation |

### 2.5 Team and Partnerships

**Lead PI: Yacine Benhamou (Prime.AI, France)**
- 21 multi-agent AI systems deployed in production
- Expertise: A2A/MCP protocols, agentic AI architecture
- Role: System architecture, orchestration, project coordination

**Co-PI: [US Academic Partner — TBD]**
Required: A US-based co-PI at an eligible NSF institution
Suggested institutions:
- MIT CSAIL — Computer Science and AI Laboratory
- Stanford HAI — Human-Centered AI Institute
- Johns Hopkins — Malone Center for Engineering in Healthcare
- University of Michigan — AI Lab + Rogel Cancer Center

**Clinical Partner: [US Cancer Center — TBD]**
Suggested:
- MD Anderson Cancer Center (Houston, TX)
- Memorial Sloan Kettering Cancer Center (New York, NY)
- Dana-Farber Cancer Institute (Boston, MA)

> **NOTE**: NSF requires a US-based lead institution. Prime.AI can participate as international collaborator or through a US subsidiary. The US academic co-PI would serve as the official PI at the NSF-eligible institution.

### 2.6 Broader Impacts

1. **Workforce Development**: Training 5 graduate students and 5 postdocs in multi-agent AI for biomedicine
2. **Curriculum**: Development of graduate course modules on "AI Agents for Digital Health"
3. **Diversity**: Recruitment plan targeting underrepresented groups in AI and oncology
4. **Open Science**: Platform open-sourced, datasets shared via NCBI/SRA and Zenodo
5. **Industry Engagement**: Advisory board including 3+ pharmaceutical companies
6. **Policy**: White paper on regulatory considerations for AI-driven clinical decision support

---

## 3. Budget Summary

| Category | Year 1 | Year 2 | Year 3 | Total |
|----------|--------|--------|--------|-------|
| Senior Personnel | $80K | $85K | $90K | $255K |
| Postdoctoral Researchers (2) | $120K | $125K | $130K | $375K |
| Graduate Students (2) | $70K | $75K | $75K | $220K |
| Cloud Computing (GPU) | $120K | $150K | $150K | $420K |
| Travel & Conferences | $30K | $35K | $40K | $105K |
| Equipment | $50K | $20K | $10K | $80K |
| Materials & Supplies | $20K | $25K | $25K | $70K |
| Subcontracting (Prime.AI) | $80K | $100K | $120K | $300K |
| Indirect Costs (F&A) | $30K | $85K | $60K | $175K |
| **Total** | **$600K** | **$700K** | **$700K** | **$2,000K** |

---

## 4. NSF Submission Requirements

| Requirement | Status |
|-------------|--------|
| Project Summary (1 page) | ✅ Complete |
| Project Description (15 pages) | ✅ Draft ready |
| References Cited | ⬜ To compile |
| Biographical Sketches (all PIs) | ⬜ Need US co-PI |
| Budget & Budget Justification | ✅ Draft ready |
| Current and Pending Support | ⬜ Need from all PIs |
| Data Management Plan (2 pages) | ⬜ To write |
| Facilities, Equipment & Resources | ⬜ Need from US institution |
| Postdoctoral Mentoring Plan | ⬜ To write |
| Collaboration Plan | ⬜ Need US co-PI input |

### Key Eligibility Notes
- **PI must be at US institution** — Prime.AI participates as subawardee/international collaborator
- **Convergence Accelerator phases**: Phase 1 ($750K/9mo) → Phase 2 ($5M/3yr) if selected
- **Submission portal**: Research.gov
- **Deadline**: Check NSF 26-XXX solicitation (anticipated spring 2026)

---

## 5. Partner Outreach Emails

### Email to Potential US Academic Co-PI

**Subject: NSF Convergence Accelerator — Multi-Agent AI Digital Twins for Cancer (seeking US Co-PI)**

Dear Professor [Name],

I'm writing to propose a collaboration on an NSF Convergence Accelerator proposal focused on AI-powered digital twins for precision oncology.

Prime.AI (France) has developed PRISM-Onco, a multi-agent AI system that orchestrates 8 specialized agents via Google's A2A and Anthropic's MCP protocols to create comprehensive digital twins of cancer patients. Our prototype has been validated on 3 cancer types using TCGA data.

We're seeking a US-based co-PI to lead the NSF submission (as required by NSF eligibility rules). Your work on [relevant research area] makes you an ideal partner for this project.

The proposal targets the Digital Twins for Living Systems track, with a budget of $2M over 3 years. Prime.AI would participate as international collaborator/subawardee.

Would you be available for a 30-minute call to discuss this opportunity?

Best regards,
Yacine Benhamou
Lead AI Builder — Prime.AI
yacine@prime-ai.fr | prime-ai.fr

### Email to Potential US Clinical Partner

**Subject: Multi-Agent AI Digital Twin System — Clinical Validation Partnership**

Dear Dr. [Name],

I'm reaching out regarding a clinical validation partnership for PRISM-Onco, our multi-agent AI system for precision oncology digital twins.

The system orchestrates 8 AI agents that collaborate to create patient-level models integrating genomic, proteomic, pharmacological, and clinical data. Our preliminary results on TCGA data show promising concordance with clinical outcomes across 3 cancer types.

We're preparing an NSF Convergence Accelerator proposal and seeking a clinical partner for:
1. Access to retrospective clinical cohorts (de-identified)
2. Prospective pilot integration with molecular tumor board (Year 3)
3. Clinical co-authorship on validation publications

The project is fully funded (no cost to your institution) and all data remains under your institutional control.

I'd welcome the opportunity to present our system and discuss potential collaboration.

Best regards,
Yacine Benhamou
Lead AI Builder — Prime.AI
yacine@prime-ai.fr | https://prime-ai.fr
