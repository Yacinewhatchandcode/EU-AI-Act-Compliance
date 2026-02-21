# NCI ITCR — Informatics Technology for Cancer Research
## NIH / National Cancer Institute
### U01 Research Project — Innovative Tools for Cancer Informatics

---

## Project Title
**PRISM-Onco: An Open-Source Multi-Agent AI Platform for Integrative Cancer Research**

---

## 1. Specific Aims

Cancer researchers increasingly rely on computational tools to analyze multi-omics data, mine literature, identify therapeutic targets, and design clinical trials. However, these tools operate in isolation, requiring researchers to manually transfer data between platforms and integrate results across modalities. This fragmentation wastes time, introduces errors, and limits the scope of analysis.

We propose to develop PRISM-Onco, an open-source multi-agent AI platform that unifies cancer informatics through autonomous agent collaboration. Building on the industrial A2A (Agent-to-Agent) and MCP (Model Context Protocol) standards, PRISM-Onco orchestrates 8 specialized AI agents that work together to conduct integrative cancer research.

**Aim 1: Develop and release an open-source multi-agent platform for cancer informatics (Years 1-2)**
We will implement PRISM-Onco as a modular, extensible platform where each of 8 specialized agents handles a distinct informatics task (genomic analysis, pathway mapping, literature mining, drug target ID, clinical trial matching, etc.). The platform will use standardized APIs (A2A, MCP) allowing the research community to add new agents or replace existing ones.

- Sub-aim 1a: Implement 8 domain-specific agents with validated performance benchmarks
- Sub-aim 1b: Develop the SAM orchestrator for multi-agent task coordination
- Sub-aim 1c: Create a web-based user interface for non-technical researchers
- Milestone: v1.0 release on GitHub with full documentation (Month 18)

**Aim 2: Validate the platform on 5 cancer types using TCGA and GDC data (Years 2-3)**
We will benchmark PRISM-Onco against established single-tool workflows (cBioPortal, QIAGEN IPA, STRING, etc.) on standardized tasks across 5 cancer types. We will measure accuracy, completeness, and time-to-insight.

- Sub-aim 2a: Define standardized evaluation tasks and metrics
- Sub-aim 2b: Conduct comparative evaluation on breast, lung, pancreatic, colorectal, and brain cancer datasets
- Sub-aim 2c: Publish benchmark datasets and results for community use
- Milestone: Validation paper submitted to Bioinformatics or Nature Methods (Month 30)

**Aim 3: Deploy the platform for community use and evaluate adoption (Year 3)**
We will deploy PRISM-Onco as a cloud-hosted service and distribute it to 10+ cancer research institutions. We will evaluate usability, adoption, and scientific output.

- Sub-aim 3a: Cloud deployment with user authentication and data privacy
- Sub-aim 3b: Training workshops at 5 NCI-designated cancer centers
- Sub-aim 3c: Collect and analyze usage data and researcher feedback
- Milestone: Community deployment with 100+ active users (Month 36)

---

## 2. Research Strategy

### 2.1 Significance

The ITCR program supports development of informatics tools that accelerate cancer research. PRISM-Onco directly addresses the key challenge identified by the cancer informatics community: **tool fragmentation**. Researchers currently use:
- cBioPortal for genomic exploration
- QIAGEN IPA or Reactome for pathway analysis
- PubMed/Semantic Scholar for literature search
- SwissDock/AutoDock for molecular docking
- REDCap for clinical data
- R/Python for statistical analysis

Each tool requires different inputs, formats, and expertise. PRISM-Onco provides a single entry point where agents automatically handle format conversion, data transfer, and result integration.

**Alignment with ITCR goals:**
- Develops new informatics tools for cancer research ✓
- Addresses data integration challenges ✓
- Promotes open-source and FAIR principles ✓
- Supports multi-institutional collaboration ✓

### 2.2 Innovation

1. **First multi-agent informatics platform for cancer**: No existing tool orchestrates multiple AI agents for integrated cancer analysis
2. **Standardized agent protocols**: Using A2A and MCP ensures interoperability with the broader AI ecosystem
3. **Emergent analysis**: Multi-agent collaboration produces insights not possible with individual tools
4. **Natural language interface**: Researchers describe their question in plain English; agents determine the analysis plan

### 2.3 Approach

**Agent Architecture:**
Each agent is implemented as an independent service with:
- A specialized LLM (fine-tuned on domain-specific corpus)
- Tool integrations (APIs to existing databases: TCGA, PubMed, UniProt, ChEMBL, ClinicalTrials.gov)
- A2A-compliant communication interface
- MCP-compatible context sharing

**Agent Specifications:**

| Agent | Data Sources | Key Tools | Output |
|-------|-------------|-----------|--------|
| Genomics | TCGA, GDC, gnomAD | bcftools, GATK, DeepVariant | Variant report, TMB, signatures |
| Proteomics | UniProt, PDB, AlphaFold | ColabFold, FPocket | Druggable targets, structures |
| Literature | PubMed, bioRxiv, PMC | PubMed API, NLP extraction | Knowledge graph, evidence scores |
| Drug Design | ChEMBL, DrugBank, ZINC | RDKit, AutoDock, ADMET predictors | Candidate molecules, ADMET profiles |
| Pathways | KEGG, Reactome, STRING | Network analysis, enrichment | Pathway maps, synthetic lethality |
| Clinical | ClinicalTrials.gov, cBioPortal | Statistical modeling | Trial matches, survival analysis |
| Digital Twin | PhysiCell, PK/PD models | ODE solvers, immune simulators | Treatment response predictions |
| Writer | All agent outputs | Template engine, NLG | Structured reports, figures |

**Orchestration:**
The SAM orchestrator:
1. Receives a research question from the user
2. Decomposes it into sub-tasks
3. Assigns tasks to appropriate agents
4. Manages data flow between agents
5. Resolves conflicts via Bayesian consensus
6. Synthesizes final report

**Validation Plan:**

| Cancer Type | n (TCGA) | Key Questions |
|-------------|----------|---------------|
| Breast (HER2+) | 500 | Treatment selection, resistance mechanisms |
| Lung (NSCLC) | 400 | Driver mutation targeting, immunotherapy prediction |
| Pancreatic | 300 | Novel targets in KRAS-mutant tumors |
| Colorectal (MSI) | 600 | MSI-H vs MSS treatment stratification |
| Glioblastoma | 250 | BBB-penetrant drug design, TMZ resistance |

**Comparison baseline tools:**
- cBioPortal (genomic analysis)
- QIAGEN IPA (pathway analysis)
- Standard PubMed search (literature)
- SwissDock (drug-target interaction)

**Evaluation metrics:**
| Metric | Definition |
|--------|-----------|
| Accuracy | % of correct therapeutic recommendations vs. literature consensus |
| Completeness | # of relevant data points integrated vs. manual analysis |
| Speed | Time to complete standard analysis workflow |
| Novelty | # of non-obvious connections identified |
| Usability | SUS (System Usability Scale) score from end users |

---

## 3. Budget

### Budget Justification ($275,000/year × 3 years = $825,000 total)

| Category | Year 1 | Year 2 | Year 3 | Total |
|----------|--------|--------|--------|-------|
| PI effort (15%) | $25K | $27K | $28K | $80K |
| Postdoc (1.0 FTE) | $55K | $57K | $60K | $172K |
| Graduate Student (0.5 FTE) | $30K | $32K | $33K | $95K |
| Cloud Computing (GPU) | $60K | $60K | $50K | $170K |
| Travel (conferences, workshops) | $15K | $15K | $20K | $50K |
| Software licenses & data access | $10K | $10K | $10K | $30K |
| Publication costs | $5K | $8K | $10K | $23K |
| Equipment | $30K | $5K | $5K | $40K |
| Subcontract (Prime.AI) | $30K | $40K | $40K | $110K |
| Indirect costs | $15K | $21K | $19K | $55K |
| **Total** | **$275K** | **$275K** | **$275K** | **$825K** |

> Note: NCI ITCR U01 awards typically range $150K-$500K/year. $275K/year is within standard range.

---

## 4. Timeline

| Quarter | Activities |
|---------|-----------|
| Y1 Q1-Q2 | Agent architecture design • A2A/MCP implementation • Genomics agent development |
| Y1 Q3-Q4 | Remaining 7 agents • SAM orchestrator • Internal testing |
| Y2 Q1-Q2 | Platform v1.0 release • GitHub documentation • Breast + lung validation |
| Y2 Q3-Q4 | Pancreatic + colorectal + GBM validation • Benchmark publication |
| Y3 Q1-Q2 | Cloud deployment • User interface polish • Training workshops |
| Y3 Q3-Q4 | Adoption evaluation • Community feedback • Sustainability plan |

---

## 5. NIH Submission Requirements

| Requirement | Status | Notes |
|-------------|--------|-------|
| PHS 398 cover page | ⬜ | Via eRA Commons |
| Project Summary/Abstract | ✅ | See Specific Aims |
| Project Narrative (2-3 sentences) | ⬜ | To write |
| Specific Aims (1 page) | ✅ | Complete |
| Research Strategy (12 pages) | ✅ | Draft complete |
| Bibliography | ⬜ | To compile |
| Budget & Justification | ✅ | Draft complete |
| Biosketch (all key personnel) | ⬜ | Need US PI |
| Facilities & Equipment | ⬜ | Need from US institution |
| Resource Sharing Plan | ⬜ | GitHub + Zenodo |
| Data Management Plan | ⬜ | To write |
| Authentication of Key Resources | ⬜ | To write |
| Letters of Support | ⬜ | From collaborating institutions |

### Key Eligibility Notes

- **PI must be at US institution** eligible for NIH funding
- Prime.AI participates as **foreign subcontract** or through a US subsidiary
- NCI ITCR Program Announcement: PAR-23-150 (or successor PAR in 2026)
- **Receipt dates**: Standard NIH dates (February, June, October)
- **Review**: NCI Special Emphasis Panel

---

## 6. Partner Outreach Email

**Subject: NCI ITCR Collaboration — Open-Source Multi-Agent AI Platform for Cancer Research**

Dear Professor [Name],

I'm reaching out to explore a collaboration on an NCI ITCR (Informatics Technology for Cancer Research) U01 proposal.

Prime.AI has developed PRISM-Onco, a multi-agent AI platform that orchestrates 8 specialized agents for integrated cancer informatics. The system automates workflows that currently require researchers to manually use 5-10 separate tools (cBioPortal, IPA, PubMed, docking, etc.).

We're seeking a US-based PI at an NIH-eligible institution to lead the submission. Prime.AI would participate as foreign subcontractor ($110K over 3 years) and provide the core AI system.

The platform will be fully open-source (Apache 2.0) and aligned with NCI's mission to accelerate cancer informatics.

Total budget: $825K over 3 years ($275K/year).

Would you be interested in discussing this partnership?

Best regards,
Yacine Benhamou
Lead AI Builder — Prime.AI
yacine@prime-ai.fr | https://prime-ai.fr
