# CIFRE Convention — Dossier de Candidature
## Convention Industrielle de Formation par la Recherche (ANRT)

---

## 1. Identification de l'Entreprise

| Champ | Valeur |
|-------|--------|
| **Raison sociale** | PRIME.AI (EURL) |
| **SIRET** | 990 020 893 00014 |
| **Adresse** | 78700 Conflans-Sainte-Honorine |
| **Secteur d'activité** | Intelligence artificielle / Santé numérique |
| **Code NAF** | 6201Z — Programmation informatique |
| **Effectif** | 1-10 salariés |
| **Chiffre d'affaires** | < 2M€ |
| **Contact** | Yacine Benhamou, Gérant |
| **Email** | yacine@prime-ai.fr |
| **Site web** | https://prime-ai.fr |

---

## 2. Laboratoire de Recherche Partenaire

### Option A — INSERM U900 (Institut Curie / Mines ParisTech)
- **Directeur** : Pr. Emmanuel Barillot
- **Spécialité** : Bioinformatique et biologie computationnelle des cancers
- **Localisation** : Paris 5e
- **Pourquoi** : Leader français en bioinformatique du cancer, expertise en intégration multi-omique

### Option B — LAMSADE (Université Paris-Dauphine / PSL)
- **Directeur** : Pr. Jérôme Lang
- **Spécialité** : IA, systèmes multi-agents, aide à la décision
- **Localisation** : Paris 16e
- **Pourquoi** : Expertise reconnue en systèmes multi-agents et IA

### Option C — MICS (CentraleSupélec)
- **Directeur** : Pr. Frédéric Pascal
- **Spécialité** : Mathématiques et informatique pour les systèmes complexes
- **Localisation** : Gif-sur-Yvette (91)
- **Pourquoi** : Intersection ML, systèmes complexes, applications santé

> **Recommandation** : Option A (INSERM U900) combine l'expertise cancer + IA computationnelle, idéale pour PRISM-Onco.

---

## 3. Sujet de Thèse

### Titre
**« Systèmes Multi-Agents à base de Grands Modèles de Langage pour l'Oncologie de Précision : Architecture, Orchestration et Validation Clinique »**

### Titre anglais
*"Large Language Model-based Multi-Agent Systems for Precision Oncology: Architecture, Orchestration and Clinical Validation"*

### Résumé (max 4000 caractères)

L'oncologie de précision repose sur l'intégration de données multi-omiques massives (génomique, transcriptomique, protéomique) pour adapter le traitement au profil moléculaire de chaque patient. Cependant, cette intégration reste largement manuelle, fragmentée et limitée par les capacités cognitives humaines face à l'explosion des données biomédicales.

Cette thèse CIFRE propose de développer et valider PRISM-Onco, un système d'intelligence artificielle multi-agents pour automatiser et accélérer la recherche en cancérologie. Le système orchestre 8 agents IA spécialisés, chacun pilotant un grand modèle de langage (LLM) finement ajusté, qui collaborent via les protocoles standardisés A2A (Agent-to-Agent, Google DeepMind) et MCP (Model Context Protocol, Anthropic).

**Axe 1 — Architecture multi-agents pour la recherche biomédicale**
Le premier axe définit une architecture formelle pour les systèmes multi-agents en oncologie. Nous modélisons les interactions entre agents comme un système distribué asynchrone avec garanties de cohérence. Chaque agent possède un domaine d'expertise (génomique, protéomique, littérature, drug design, voies de signalisation, essais cliniques, jumeau numérique, rédaction scientifique) et communique ses résultats via des protocoles standardisés. L'enjeu scientifique est de démontrer que la collaboration inter-agents produit des insights émergents — des hypothèses de recherche qu'aucun agent individuel ne peut générer seul.

**Axe 2 — Orchestration et raisonnement collectif**
Le deuxième axe développe les mécanismes d'orchestration : allocation dynamique de tâches, résolution de conflits entre agents, et agrégation des résultats. Nous introduisons un protocole de consensus bayésien pour pondérer les recommandations des agents spécialisés selon leur confiance et leur expertise. L'orchestrateur (Agent SAM, développé par Prime.AI) coordonne les pipelines de recherche et gère les dépendances entre analyses.

**Axe 3 — Validation clinique rétrospective**
Le troisième axe valide le système sur des cohortes cliniques réelles. En collaboration avec l'INSERM U900 / Institut Curie, nous comparerons les recommandations thérapeutiques de PRISM-Onco aux décisions cliniques effectives sur 3 indications : cancer du sein HER2+, NSCLC à mutation EGFR, et adénocarcinome pancréatique. Les métriques d'évaluation incluent : concordance avec les décisions du tumor board, identification de cibles thérapeutiques validées, et qualité des molécules candidates générées.

**Contributions attendues :**
1. Cadre formel pour les systèmes multi-agents LLM en biomédecine
2. Protocole d'orchestration avec consensus bayésien
3. Benchmark de validation clinique sur 3 cancers
4. Plateforme open-source PRISM-Onco (TRL 4→6)
5. 3-5 publications dans des revues à comité de lecture (Nature Methods, Bioinformatics, JMLR)

### Mots-clés
Multi-agent systems, Large Language Models, Precision Oncology, Drug Discovery, Digital Twin, A2A Protocol, MCP Protocol, Computational Biology

---

## 4. Profil du Doctorant Recherché

| Critère | Exigence |
|---------|----------|
| **Diplôme** | Master 2 / École d'ingénieur (Bac+5) |
| **Spécialité** | IA / Machine Learning / Bioinformatique |
| **Compétences techniques** | Python, PyTorch/JAX, NLP/LLM, APIs biomédicales |
| **Compétences souhaitées** | Systèmes distribués, biologie computationnelle |
| **Langues** | Français + Anglais scientifique courant |
| **Qualités** | Autonomie, rigueur scientifique, créativité |

### Écoles doctorales compatibles
- **ED 515 — Complexité du Vivant** (Sorbonne Université)
- **ED 386 — Sciences Mathématiques de Paris Centre** (PSL)
- **ED 580 — STIC** (CentraleSupélec / Université Paris-Saclay)

---

## 5. Programme de Travail (36 mois)

### Année 1 — Fondations (Mois 1-12)
| Semestre | Activités |
|----------|-----------|
| S1 | État de l'art multi-agents + LLM en biomédecine • Formalisation de l'architecture PRISM-Onco • Formation aux outils du laboratoire |
| S2 | Implémentation du protocole d'orchestration • Premier prototype des 8 agents spécialisés • Publication 1 : survey/position paper |

### Année 2 — Développement (Mois 13-24)
| Semestre | Activités |
|----------|-----------|
| S3 | Consensus bayésien inter-agents • Intégration données TCGA/GDC • Validation sur cancer du sein HER2+ |
| S4 | Extension NSCLC + pancréas • Publication 2 : architecture paper • Conférence MICCAI ou NeurIPS Workshop |

### Année 3 — Validation & Rédaction (Mois 25-36)
| Semestre | Activités |
|----------|-----------|
| S5 | Validation clinique rétrospective avec Institut Curie • Benchmark comparatif • Publication 3 : validation paper |
| S6 | Rédaction du manuscrit de thèse • Publication 4-5 : résultats finaux • Soutenance (M36) |

---

## 6. Encadrement

### Directeur de thèse (Académique)
- **Nom** : [À définir — contacter INSERM U900]
- **HDR** : Oui (obligatoire)
- **Taux d'encadrement** : 50%

### Co-encadrant industriel (Prime.AI)
- **Nom** : Yacine Benhamou
- **Fonction** : Gérant / Lead AI Builder
- **Expertise** : 21 systèmes multi-agents déployés, architecture A2A/MCP
- **Taux d'encadrement** : 50%

### Comité de suivi de thèse
- Réunion semestrielle
- Membres : directeur de thèse + co-encadrant + 1 expert externe

---

## 7. Budget & Financement CIFRE

| Poste | Montant annuel | Total (3 ans) |
|-------|---------------|---------------|
| **Salaire brut doctorant** | ~28 000 € | 84 000 € |
| **Charges patronales** | ~12 000 € | 36 000 € |
| **Coût total employeur** | ~40 000 € | 120 000 € |
| **Subvention ANRT** | -14 000 € | -42 000 € |
| **Coût net Prime.AI** | ~26 000 € | **78 000 €** |

### Autres coûts pris en charge par Prime.AI
| Poste | Budget |
|-------|--------|
| Infrastructure cloud (GPU) | 15 000 €/an |
| Conférences et déplacements | 5 000 €/an |
| Abonnements données/outils | 3 000 €/an |
| **Total sur 3 ans** | **69 000 €** |

### Coût total CIFRE pour Prime.AI : **~147 000 €** sur 3 ans
### Subvention ANRT : **42 000 €** + Crédit Impôt Recherche (CIR) potentiel

---

## 8. Retombées Attendues

### Pour Prime.AI
1. **Propriété intellectuelle** : brevets sur l'architecture multi-agents
2. **Produit** : plateforme PRISM-Onco TRL 6 → commercialisable
3. **Recrutement** : intégration du doctorant en CDI post-thèse
4. **CIR** : éligibilité au Crédit Impôt Recherche (~30% des dépenses)
5. **Crédibilité** : publications académiques = validation scientifique

### Pour le laboratoire
1. Accès à l'infrastructure multi-agents de Prime.AI
2. Publications co-signées
3. Exploration d'une nouvelle méthodologie de recherche
4. Perspective de transfert technologique

### Pour la société
1. Accélération de la recherche en cancérologie
2. Démocratisation de l'IA de précision
3. Souveraineté technologique française en IA santé

---

## 9. Pièces Justificatives à Fournir

### Par Prime.AI
- [ ] Kbis de moins de 3 mois
- [ ] Liasse fiscale (2 derniers exercices)
- [ ] CV du co-encadrant industriel (Yacine Benhamou)
- [ ] Lettre d'engagement de financement
- [ ] Description du projet de recherche (ce document)

### Par le laboratoire
- [ ] Lettre d'accord du directeur de laboratoire
- [ ] CV du directeur de thèse (HDR)
- [ ] Avis de l'école doctorale

### Par le doctorant
- [ ] CV + lettre de motivation
- [ ] Relevés de notes M1/M2
- [ ] Lettre(s) de recommandation

---

## 10. Calendrier de Soumission

| Étape | Date | Responsable |
|-------|------|-------------|
| Contact laboratoire partenaire | Février-Mars 2026 | Yacine |
| Identification du doctorant | Mars-Mai 2026 | Labo + Yacine |
| Inscription école doctorale | Juin 2026 | Doctorant |
| Soumission dossier ANRT | Juillet 2026 | Yacine + Labo |
| Réponse ANRT (~3 mois) | Octobre 2026 | ANRT |
| Début de la thèse | Novembre 2026 | Doctorant |

---

## 11. Contact pour Soumission

**ANRT — Association Nationale de la Recherche et de la Technologie**
- Site : https://www.anrt.asso.fr/fr/cifre-702
- Email : cifre@anrt.asso.fr
- Téléphone : 01 55 35 25 50
- Dépôt en ligne : https://www.anrt.asso.fr/fr/deposer-une-cifre

---

## Emails de Contact Laboratoires (Prêts à Envoyer)

### Email pour INSERM U900 (Institut Curie)

**Objet : Proposition de thèse CIFRE — Systèmes Multi-Agents IA pour l'Oncologie de Précision**

Madame, Monsieur,

Je me permets de vous contacter au sujet d'un projet de thèse CIFRE que nous souhaitons développer en partenariat avec votre unité.

Prime.AI est une entreprise spécialisée en intelligence artificielle agentique. Nous avons développé PRISM-Onco, un système multi-agents orchestrant 8 agents IA spécialisés pour accélérer la recherche en cancérologie. Le système utilise les protocoles A2A (Google) et MCP (Anthropic) pour coordonner des analyses génomiques, protéomiques, de littérature, et de conception de médicaments.

Nous recherchons un laboratoire partenaire pour encadrer une thèse CIFRE de 3 ans portant sur la formalisation, l'orchestration et la validation clinique de ce système. Votre expertise en bioinformatique du cancer et en intégration multi-omique est idéalement complémentaire à notre compétence en architecture multi-agents.

Le financement CIFRE couvre le salaire du doctorant (subvention ANRT de 14 000€/an), et Prime.AI prend en charge l'infrastructure cloud, les conférences et les outils.

Seriez-vous disponible pour un échange de 30 minutes afin de discuter de cette opportunité ?

Cordialement,

Yacine Benhamou
Gérant — Prime.AI
yacine@prime-ai.fr | prime-ai.fr
Tél. : [votre numéro]

### Email pour LAMSADE (Paris-Dauphine)

**Objet : Proposition CIFRE — Architecture Multi-Agents LLM pour Applications Biomédicales**

Madame, Monsieur,

Prime.AI développe des systèmes d'IA multi-agents pour des applications critiques. Notre projet phare, PRISM-Onco, orchestre 8 agents IA spécialisés via les protocoles A2A et MCP pour la recherche en oncologie.

Nous cherchons à formaliser cette architecture dans le cadre d'une thèse CIFRE, en collaboration avec un laboratoire expert en systèmes multi-agents et en IA. Le LAMSADE représente pour nous le partenaire académique idéal grâce à votre travail reconnu sur les systèmes multi-agents et l'aide à la décision.

La thèse porterait sur : (1) la formalisation de l'architecture multi-agents LLM, (2) les mécanismes d'orchestration et de consensus, et (3) la validation sur des données cliniques en oncologie.

Financement CIFRE (ANRT) + infrastructure cloud fournie par Prime.AI.

Seriez-vous intéressé par un échange ?

Cordialement,
Yacine Benhamou — Prime.AI
