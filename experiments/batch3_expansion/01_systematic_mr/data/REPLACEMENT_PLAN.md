# Pair-by-Pair Data Replacement Plan

## Overview

71 pairs. Currently 5 have fully exact data, 66 have at least one approximate stratum.
All 44 transport pairs have approximate data → Q < 1 by construction (circular).

This plan distinguishes:
- **Tier 1 — Published MR estimates**: Papers report per-ancestry IVW beta/SE directly. Plug into pairs_curated.json.
- **Tier 2 — GWAS available, MR needs computation**: Consortia ship per-ancestry summary stats. Must run 2-sample MR ourselves per ancestry.
- **Tier 3 — Domain-knowledge only**: No multi-ancestry data. Mark explicitly in paper.

Sources key:
- **Wang 2022** = Genome Medicine PMC9195360: 37 factors → CAD, EAS (BBJ) vs EUR (UKBB)
- **GLGC 2021** = Global Lipids Genetics Consortium, 5 ancestries, 1.65M individuals
- **T2DGGI 2024** = Suzuki et al. Nature, 5 ancestries, built-in MR-MEGA het p
- **MVP 2024** = Million Veteran Program, 2068 traits, 4 populations
- **PGC** = Psychiatric Genomics Consortium, ancestry-specific files downloadable
- **CKDGen** = trans-ethnic vs EA CKD files
- **MEGASTROKE** = multi-ancestry stroke GWAS
- **PAGE** = 26 phenotypes, non-European focus
- **Ishigaki 2022** = RA multi-ancestry, separate EAS file
- **PRACTICAL** = prostate cancer, 4 ancestries
- **BCAC/BBJ×UKB** = breast/pan-cancer, EAS vs EUR harmonized
- **Asthma exac.** = Zenodo 5513443, ships pre-computed Cochran's Q
- **Circ 2025** = CKB Circulation PMC12165552, Lp(a) → MI/stroke
- **O'Loughlin 2023** = BMC Medicine PMC9893684 (previously misattributed as "Cheng 2023"), BMI → depression EAS
- **PD multi-anc** = 49K cases, 4 ancestries, Google Drive download
- **Depression 2025** = Nat Hum Behav, cross-ancestry depression meta
- **IL6R MVP** = medrxiv 2022.09.24.22280325, IL6R variant AFR vs EUR explicit stratum-specific estimates
- **Pancreatic MEC** = PMID 32958499, Multiethnic Cohort 5-ancestry per-ancestry ORs, het p=0.12
- **Wang 2023 VitD** = cnsgenomics.com, per-ancestry GWAS files (AFR/EAS/SAS), UKBB-based
- **CRP 2025** = Nat Commun 2025 s41467-025-59155-w, 513K genomes sequencing-based, ancestry-specific
- **CRP 2014** = PMID 24622110, multi-ancestry replication in AFR and HISP
- **Telomere 2024** = PMID 38789417, 211K multi-ancestry telomere length meta-analysis
- **Urate CKD trans-ethnic** = Heliyon 2023 PMID 37908715, exact per-ancestry β (EUR/AFR/Asian), opposite signs
- **LDL stroke 2025** = rs.3.rs-6091701/v1, multi-ancestry MR methods paper, LDL→stroke worked example
- **VitD T2D** = UCL 10141625, bidirectional MR EUR vs South Asian, exact numbers
- **BMI gastric** = Springer 10.1007/s10120-023-01439-5, ethnic-specific MR EUR vs Korean
- **Neutrophil lung** = PMID 39744580, EUR OR=1.027 vs EAS OR=1.223
- **BMI EAS PheWAS** = PMC12212858, phenome-wide BMI MR in East Asians, multi-pair source
- **Problematic alcohol** = medrxiv 2023.01.24.23284960v2, 1M+ multi-ancestry GWAS
- **SLE cancer** = CMJ 2023, trans-ethnic MR, opposite cancer types per ancestry
- **Telomere lung Asian** = WJON 1624, Asian-specific MR telomere→lung cancer
- **Ogawa 2019 psoriasis** = J Invest Dermatol PMC7028352, 9 metabolic traits → psoriasis, EUR + JPN IVW β/SE
- **CETP 2024** = Nature Commun PMC11192935, drug-target MR, 18 outcomes EUR vs EAS, Figs 3-4 verified
- **Neutrophil lung 2025** = J Cancer PMC11660127, EUR + EAS IVW β/SE for NC → lung cancer
- **Hemani 2025 CAMeRa** = doi:10.21203/rs.3.rs-6091701/v1, cross-ancestry MR framework
- **Ogawa 2019** = J Invest Dermatol PMC7028352, 9 metabolic traits → psoriasis trans-ethnic
- **Zhu 2023 SLE** = Chinese Med J, SLE → 3 female cancers, EUR vs EAS IVW ORs
- **Tyrrell 2019** = Int J Epidemiol 48(3):834-848, BMI → depression EUR. OR=1.18 (1.09-1.28). Swap script had wrong OR=1.08
- **Ooi 2019** = Int J Epidemiol PMC6659372, BMI→breast cancer EUR, BCAC 228,951, IVW OR=0.81 (0.74-0.89)
- **Wu 2025** = Medicine Baltimore PMID 40587687, BMI→breast cancer EAS PheWAS, IVW OR=0.67 (0.53-0.84)
- **Austin-Zimmerman 2026** = Biol Psychiatry Global Open Sci PMID 42181294, CUD↔psychosis bidirectional MR. Uses cross-ancestry CUD GWAS (Nat Genet 2023). Pooled MR: CUD→psychosis β=0.31 (0.22-0.41). Per-ancestry stratification unknown — need supplement
- **Urate cross-ancestry 2024** = N=1,029,323 cross-ancestry serum urate meta-analysis with ancestry-specific MR on urate-correlated diseases. Need supplement for gout specifically
- **Johnson 2024** = Neuropsychopharmacol, SCZ/cannabis/smoking cross-ancestry. MR is EUR-ONLY (AFR underpowered). NOT useful for cannabis→SCZ
- **Park 2023 gastric** = Gastric Cancer 26:1044-1053, BMI → GC. EUR IVW OR=1.10; Korean IVW OR=1.00 (null, U-shaped nonlinear)
- **Su 2022 smoking SCZ** = Schizophrenia 2022:72, smoking → SCZ EAS. IVW OR=4.00 (0.89-18.01), p=0.071
- **Cho 2024 urate GWAS** = Nat Commun 15:3441, N=1M cross-ancestry urate GWAS. MR is POOLED, not per-ancestry. Tier 2 source only
- **Smith 2023 T2DGGI** = medRxiv 2023.09.28.23296294, T2D genetic subtypes. NOT MR. Discussion context for BMI→T2D non-transport
- **Zhan 2025 AD** = J Transl Med 23:278, proteome-wide MR protein→AD. EUR has 5 causal proteins, AFR has ZERO (but 15× power deficit)
- **Wang 2023 prostate** = Nat Genet 55(12):2065-2074, PRACTICAL multi-ancestry GWAS/GRS. NOT MR. Cannot help height→prostate
- **Li 2025 breast** = medRxiv 2025.08.20.25334075, multi-ancestry breast cancer GWAS. NOT MR
- **Zhao 2022 GBMI** = Cell Genomics 2:100195, proteome-wide MR 1,310 EUR + 1,311 AFR proteins × 8 diseases. 45 EUR + 7 AFR signals. 7 trans-ancestry, 89 EUR-specific, 12 AFR-specific. SERPINE2→VTE EUR OR=0.94, AFR OR=0.82. ACE→COPD validated in AFR (OR=0.88). Tables S7/S8/S16 have full per-ancestry ORs

---

## Cardiometabolic (18 pairs)

| # | Pair ID | Expected | Current exact/approx | Tier | Source | Action |
|---|---------|----------|---------------------|------|--------|--------|
| 1 | LDL_CAD_MR | transport | 1/3 | **1** | Wang 2022 (EAS OR=1.77, EUR OR=1.82) | Replace. Q=0.07, confirmed transport |
| 2 | HDL_CAD_MR | transport | 1/3 | **1** | Wang 2022 (EAS OR=0.89, EUR OR=0.89) | Replace. Q=0.00, confirmed transport |
| 3 | triglycerides_CAD_MR | transport | 1/2 | **1** | Wang 2022 (EAS OR=1.44, EUR OR=1.27) | Replace. Q=0.48, confirmed transport |
| 4 | SBP_CAD_MR | transport | 1/3 | **1** | Wang 2022 (EAS OR=1.68, EUR OR=1.96) | Replace. Q=1.40, confirmed transport |
| 5 | T2D_CAD_MR | transport | 1/3 | **1** | Wang 2022 (EAS OR=1.13, EUR OR=1.08) | Replace. Q=2.32, confirmed transport |
| 6 | BMI_CAD_MR | non-transport | 1/3 | **1** | Wang 2022 (EAS OR=1.67, EUR OR=1.38) | Replace. Q=7.27, confirmed non-transport |
| 7 | Lp_a_CAD_MR | transport | 1/2 | **1** | Circ 2025 (EAS RR=0.78, EUR RR=0.78) | Replace. Q=0.00, confirmed transport |
| 8 | BMI_T2D_MR | non-transport | 1/3 | **1** | T2DGGI 5-ancestry + **CAMeRa 2025 (Hemani preprint rs-6091701)**: EAS logOR=0.66 (SE=0.08) vs EUR logOR=0.99 (SE=0.07), Q p=0.002. CONFIRMED non-transport with proper instruments. | **DONE** — added to swap script |
| 9 | WHR_T2D_MR | non-transport | 1/3 | **2** | T2DGGI | Run per-ancestry MR |
| 10 | fasting_glucose_T2D_MR | transport | 1/2 | **2** | T2DGGI | Run per-ancestry MR |
| 11 | SBP_stroke_MR | transport | 1/3 | **2** | MEGASTROKE multi-ancestry | Run per-ancestry MR |
| 12 | LDL_stroke_MR | transport | 1/2 | **1** | **CAMeRa 2025 analysis repo** (github.com/yoonsucho/camera_analysis, mr.html kable). 5 ancestries: EUR logOR=0.0811 (SE=0.0185), EAS=0.0221 (0.0272), AFR=0.2852 (0.0826), AMR=0.3016 (0.2049), SAS=0.2061 (0.1778). 5-ancestry Q=12.09 (p=0.017, non-transport). EUR-vs-EAS only Q=3.21 (p=0.073, transport). Driven by AFR. | **DONE** — added to swap script |
| 13 | smoking_CAD_MR | transport | 1/2 | **2** | MVP 4-ancestry | Check MVP for per-ancestry MR |
| 14 | IL6R_CAD_MR | transport | 1/2 | **1** | IL6R MVP medrxiv 2022.09.24.22280325 (PDF downloaded as il6r_mvp_preprint_real.pdf, 3MB). **VERIFIED**: PheWAS of rs2228145 in 545K Veterans (106K AFR, 439K EUR). IHD: EUR OR=0.96 (0.95-0.97), AFR OR=0.99 (0.95-1.02). Aortic aneurysm: EUR OR=0.92 (0.90-0.94), AFR OR=0.95 (0.87-1.03). CVD concordant = TRANSPORT. | **DONE** — added to swap script |
| 15 | alcohol_CAD_MR | non-transport | 2/2 | **1** | MVP 2024 (EUR/AFR/HISP all OR~1.0) | Replace. Q=0.71, reclassify as transport or drop |
| 16 | urate_gout_MR | non-transport | 1/3 | **2** | ~~Heliyon urate→kidney~~ wrong outcome. Cho 2024 supplement inspected (ST1-ST28): ST25 has SU→gout IVW OR=4.86 (p=3e-36, 89 SNPs) but POOLED cross-ancestry, no ancestry column. **RESOLVED: stays Tier 2** | Run per-ancestry MR ourselves using Cho 2024 GWAS |
| 17 | alcohol_liver_cirrhosis_MR | non-transport | 2/1 | **3** | EUR only | Domain-knowledge |
| 18 | BMI_asthma_MR | transport | 1/3 | **2** | Asthma exac. Zenodo (has Cochran's Q!) | Best external validation check |

**Summary**: 10 Tier 1 (incl. IL6R_CAD, BMI_T2D, LDL_stroke — all in swap script), 6 Tier 2 (urate stays Tier 2 after Cho 2024 supplement check), 2 Tier 3.

---

## Cancer (11 pairs)

| # | Pair ID | Expected | Current exact/approx | Tier | Source | Action |
|---|---------|----------|---------------------|------|--------|--------|
| 19 | smoking_lung_cancer_MR | transport | 1/3 | **2** | MVP or ILCCO | Check for per-ancestry MR |
| 20 | BMI_breast_cancer_MR | non-transport | 1/3 | **1 (assembled)** | **Ooi 2019 (PMC6659372)**: EUR BCAC IVW OR=0.81 (0.74-0.89); **Wu 2025 (PMID 40587687)**: EAS PheWAS IVW OR=0.67 (0.53-0.84). Same direction (protective). Q=2.25, p=0.13 → TRANSPORT. Two independent papers, not one multi-ancestry study — flag in methods. | **DONE** — added to swap script |
| 21 | alcohol_breast_cancer_MR | transport | 1/2 | **2** | MVP | Check MVP |
| 22 | BMI_colorectal_cancer_MR | transport | 1/3 | **2** | MVP or BBJ×UKB pan-cancer | Check for per-ancestry |
| 23 | height_prostate_cancer_MR | transport | 1/2 | **2** | PRACTICAL 4-ancestry | Per-ancestry ORs reported |
| 24 | smoking_bladder_cancer_MR | transport | 1/2 | **2** | MVP | Check MVP |
| 25 | BMI_endometrial_cancer_MR | transport | 1/2 | **2** | MVP | Check MVP |
| 26 | BMI_kidney_cancer_MR | transport | 1/2 | **2** | MVP | Check MVP |
| 27 | smoking_COPD_MR | transport | 1/2 | **2** | MVP | Check MVP |
| 28 | insulin_resistance_pancreatic_cancer_MR | non-transport | 1/3 | **3** | ~~Pancreatic MEC 5-ancestry ORs~~ **CONFIRMED WRONG STUDY TYPE**: Bogumil 2020 (PMID 32958499) is a PRS/GRS replication study, NOT insulin resistance MR. Het p=0.12 is for PRS transferability. EUR-only MR exists (Carreras-Torres 2017) but no multi-ancestry MR. | Domain-knowledge only |
| 29 | telomere_length_cancer_MR | transport | 1/2 | **2** | ~~Telomere 2024 multi-ancestry 211K~~ **CONFIRMED WRONG STUDY TYPE**: PMID 38789417 is GWAS gene validation, NOT MR-on-cancer. Separate EAS lung cancer MR exists (PMC6885879) and EUR pan-cancer MR (JAMA Oncol 2017), but no single combined paper. | Assembly from separate papers or run ourselves |

**Summary**: 1 Tier 1 (BMI→breast cancer assembled), 8 Tier 2, 1 Tier 3 (pancreatic — PRS not MR), 0 already exact. Telomere source corrected (GWAS validation, not MR).

---

## Psychiatric (6 pairs)

| # | Pair ID | Expected | Current exact/approx | Tier | Source | Action |
|---|---------|----------|---------------------|------|--------|--------|
| 30 | BMI_depression_MR | non-transport | 1/3 | **1** | O'Loughlin 2023 EAS (PMC9893684, not "Cheng 2023") + Tyrrell 2019 EUR | Replace. Opposite directions! Q=36.4 |
| 31 | cannabis_schizophrenia_MR | transport | 1/2 | **2** | Austin-Zimmerman 2026 supplement inspected (mmc2.xlsx, 24 sheets). SD17-SD18 have MR-CLUST (SNP-level pleiotropy clustering) but NO per-ancestry MR stratification. MR is pooled using cross-ancestry CUD GWAS input. **RESOLVED: stays Tier 2** | Run per-ancestry MR ourselves using CUD GWAS + PGC |
| 32 | smoking_schizophrenia_MR | transport | 1/2 | **1** | **Su 2022 (PMC9463183)**: EAS smoking init→SCZ OR=4.00 (0.89-18.01) p=0.071; **Wootton 2020 (PMC7610182)**: EUR smoking init→SCZ IVW OR=1.53 (1.35-1.74) p=3.7e-11, 371 SNPs. Q=1.56, p=0.21. TRANSPORT. | **DONE** — added to swap script |
| 33 | education_schizophrenia_MR | non-transport | 1/3 | **2** | PGC SCZ | Run per-ancestry MR |
| 34 | CRP_depression_MR | transport | 1/2 | **2** | CRP 2025 513K ancestry-specific + PGC MDD | Run per-ancestry MR |
| 35 | BMI_bipolar_MR | transport | 1/2 | **2** | PGC bipolar | Run per-ancestry MR |

**Summary**: 2 Tier 1 (BMI→depression, smoking→SCZ), 4 Tier 2, 0 Tier 3.

---

## Autoimmune (10 pairs)

| # | Pair ID | Expected | Current exact/approx | Tier | Source | Action |
|---|---------|----------|---------------------|------|--------|--------|
| 36 | HLA_DRB1_RA_risk | non-transport | 3/1 | **2** | Ishigaki 2022 separate EAS file | Upgrade to independent EAS estimate |
| 37 | smoking_RA_seropositive | non-transport | 2/1 | **3** | No multi-ancestry MR | Domain-knowledge |
| 38 | sex_ratio_RA | non-transport | 3/1 | **3** | Observational, not MR | Keep as-is (mostly exact) |
| 39 | IL6_cytokine_RA_MR | non-transport | 3/0 | -- | Already fully exact | No change needed |
| 40 | RA_ILD_MR_multi_ancestry | non-transport | 2/0 | -- | Already fully exact | No change needed |
| 41 | BMI_RA_MR | transport | 1/2 | **2** | Ishigaki 2022 + EUR MR | Run per-ancestry MR |
| 42 | alcohol_RA_MR | transport | 1/2 | **3** | Sparse | Domain-knowledge |
| 43 | IL6R_RA_MR | transport | 2/1 | **3** | IL6R MVP PheWAS **VERIFIED from PDF** (il6r_mvp_preprint_real.pdf): RA is NOT among 29 differentially associated traits. Paper reports 1,875 phenotypes but RA not in heterogeneous set. Existing IL6R MR papers (Lancet 2012, npj 2019) are EUR-only for RA. | Domain-knowledge only |
| 44 | vitD_RA_MR | transport | 1/2 | **2** | Wang 2023 VitD per-ancestry GWAS (AFR/EAS/SAS) | Run per-ancestry MR |
| 45 | CRP_RA_MR | transport | 1/2 | **2** | CRP 2025 513K ancestry-specific | Run per-ancestry MR |

**Summary**: 0 Tier 1, 3 Tier 2 (HLA_DRB1_RA, BMI_RA, vitD/CRP_RA), 5 Tier 3 (IL6R_RA — paper verified but RA not among reported outcomes), 2 already exact.

---

## AD (17 pairs)

| # | Pair ID | Expected | Current exact/approx | Tier | Source | Action |
|---|---------|----------|---------------------|------|--------|--------|
| 46 | APOE4_AD_risk | non-transport | 4/0 | -- | Already fully exact (Belloy 2023) | No change needed |
| 47 | sex_tau_spread | non-transport | 4/0 | -- | Already fully exact | No change needed |
| 48 | ancestry_amyloid_threshold | non-transport | 3/1 | **3** | Partial | Keep mostly exact |
| 49 | age_lecanemab_response | non-transport | 3/0 | -- | Already fully exact | No change needed |
| 50 | APOE2_AD_protective | non-transport | 1/3 | **2** | Belloy 2023 has 4-ancestry data | Extract per-ancestry ORs |
| 51 | BMI_AD_MR | non-transport | 2/2 | **3** | Sparse AD multi-ancestry | Domain-knowledge |
| 52 | T2D_AD_MR | non-transport | 1/3 | **3** | Sparse | Domain-knowledge |
| 53 | SBP_AD_MR | non-transport | 2/2 | **3** | Sparse | Domain-knowledge |
| 54 | CRP_AD_MR | transport | 2/1 | **2** | CRP 2025 513K ancestry-specific | Run per-ancestry MR |
| 55 | TREM2_AD_causal | transport | 2/1 | **3** | EUR only | Domain-knowledge |
| 56 | education_AD_MR | transport | 1/2 | **3** | Sparse | Domain-knowledge |
| 57 | alcohol_AD_MR | transport | 1/2 | **3** | Sparse | Domain-knowledge |
| 58 | vitD_AD_MR | transport | 1/2 | **2** | Wang 2023 VitD per-ancestry GWAS (AFR/EAS/SAS) | Run per-ancestry MR |
| 59 | smoking_AD_MR | transport | 1/2 | **3** | Sparse | Domain-knowledge |
| 60 | physical_activity_AD_MR | transport | 1/2 | **3** | Sparse | Domain-knowledge |
| 61 | sleep_duration_AD_MR | transport | 1/2 | **3** | Sparse | Domain-knowledge |
| 62 | IL6_AD_MR | transport | 1/2 | **3** | Sparse | Domain-knowledge |

**Summary**: 0 Tier 1, 3 Tier 2 (APOE2, CRP_AD, vitD_AD), 11 Tier 3, 3 already exact.

---

## MS (9 pairs)

| # | Pair ID | Expected | Current exact/approx | Tier | Source | Action |
|---|---------|----------|---------------------|------|--------|--------|
| 63 | HLA_DRB1_MS_risk | non-transport | 2/2 | **3** | No multi-ancestry MS MR | Domain-knowledge |
| 64 | latitude_vitD_MS | non-transport | 2/2 | **3** | Observational only | Domain-knowledge |
| 65 | sex_ratio_MS | non-transport | 2/2 | **3** | Observational only | Domain-knowledge |
| 66 | EBV_MS_causal | transport | 1/2 | **3** | EUR only | Domain-knowledge |
| 67 | smoking_MS_MR | transport | 1/2 | **3** | EUR only | Domain-knowledge |
| 68 | vitD_MS_MR | transport | 2/1 | **2** | Wang 2023 VitD per-ancestry GWAS (AFR/EAS/SAS) | Run per-ancestry MR |
| 69 | BMI_MS_MR | transport | 1/2 | **3** | EUR only | Domain-knowledge |
| 70 | IL6_MS_MR | transport | 1/2 | **3** | EUR only | Domain-knowledge |
| 71 | gut_microbiome_MS | non-transport | 1/3 | **3** | Sparse | Domain-knowledge |

**Summary**: 0 Tier 1, 1 Tier 2 (vitD_MS), 8 Tier 3.

---

## Grand Summary

| Tier | Count | Description |
|------|-------|-------------|
| **Tier 1** | **14** | Published per-ancestry MR estimates (all 14 in swap script: 13 REPLACEMENTS + 1 alcohol separate) |
| **Tier 2** | **27** | Per-ancestry GWAS available, need to run MR ourselves |
| **Tier 3** | **24** | No multi-ancestry data, domain-knowledge only |
| **Already exact** | **6** | Fully exact strata, no changes needed |
| **Total** | **71** | |

**Tier 1 breakdown** (14 pairs, all in swap script):
- Wang 2022 ×6 (LDL/HDL/TG/SBP/T2D/BMI → CAD) — **in swap**
- CKB Lp(a) → CAD — **in swap**
- MVP alcohol → CAD — **in swap**
- O'Loughlin 2023 + Tyrrell 2019: BMI → depression — **in swap**
- IL6R MVP → CAD (EUR OR=0.96, AFR OR=0.99) — **in swap**
- Wootton 2020 + Su 2022: smoking → SCZ (EUR OR=1.53, EAS OR=4.00) — **in swap**
- Ooi 2019 + Wu 2025: BMI → breast cancer (EUR OR=0.81, EAS OR=0.67, assembled) — **in swap**
- CAMeRa 2025 BMI → T2D (EAS logOR=0.66, EUR logOR=0.99, Q p=0.002) — **in swap**
- CAMeRa 2025 LDL → stroke (5 ancestries, Q=12.09) — **IN SWAP** (exact per-ancestry betas/SEs from analysis repo HTML tables)

**Changes from initial assessment**:
- IL6R_CAD_MR: Re-verified as Tier 1 (real PDF downloaded, CVD outcomes concordant EUR/AFR)
- IL6R_RA_MR: Tier 1 → Tier 3 (paper verified but RA not among reported outcomes in PheWAS)
- urate_gout_MR: Tier 1 → Tier 2 (Heliyon paper studies urate→BUN/CKD, NOT urate→gout)
- smoking_schizophrenia_MR: Tier 2 → Tier 1 (Su 2022 has EAS OR from Taiwan Biobank + BBJ)
- BMI_T2D_MR: Tier 2 → Tier 1 (CAMeRa 2025 has per-ancestry logOR with Q p=0.002)
- LDL_stroke_MR: Tier 2 → Tier 1 (CAMeRa 2025 has per-ancestry data for 5 ancestries)
- insulin_resistance_pancreatic_cancer_MR: Tier 2 → Tier 3 (PMID 32958499 is PRS, not MR)

**Supplement checks completed (2026-07-17)**:
- **Austin-Zimmerman 2026 (cannabis)**: mmc2.xlsx 24 sheets inspected. MR-CLUST present (SD17-SD18) but NO per-ancestry MR. Stays Tier 2
- **Cho 2024 (urate)**: ST1-ST28 inspected. ST25 has SU→gout OR=4.86 but POOLED. Stays Tier 2
- **Mason et al. 2025**: Full review paper read (15 pages, arXiv:2510.17554v1). Key quotes extracted to MASON_2025_KEY_QUOTES.md

**Corrections found in this session (2026-07-17)**:
- **BMI_depression_MR EUR OR is WRONG in swap script**: Tyrrell 2019 Table 2 confirms OR=1.18 (1.09-1.28), NOT OR=1.08. Must fix in swap_tier1_real_data.py
- **cannabis_schizophrenia_MR stays Tier 2**: Johnson 2024 does NOT have per-ancestry MR (AFR too underpowered; MR was EUR-only). Cannot upgrade
- **height_prostate_MR stays Tier 2/3**: PRACTICAL (Wang 2023) is GWAS/GRS, not MR. No causal exposure→cancer estimates
- **breast_cancer pairs stay as-is**: Li 2025 is GWAS, not MR

**NEW methodological citation (from Perplexity search 2026-07-17)**:
- **Mason, Zuber, Hemani, Burgess et al. 2025** (arXiv:2510.17554): "Mendelian randomization in a multi-ancestry world: reflections and practical advice." Independent authoritative validation of our composite-hypothesis framing. Cite in Discussion.

**NEW potential domain pairs (deferred, not in this freeze)**:
- **TG→endometriosis** (PLOS ONE 2024): EUR IVW OR=1.112 p=5.03e-3, EAS null. Real cross-ancestry MR from GLGC
- **Migraine↔psychiatric** (MVP 2025): 433K multi-ancestry GWAS + MR nulls against PTSD/depression/TBI

**Papers useful for Discussion but NOT for data extraction**:
- Smith 2023 T2DGGI: Explains WHY BMI→T2D non-transportability occurs (different lipodystrophy cluster proportions by ancestry)
- Cho 2024 urate: ρ_gc=0.942 for SU genetics across EUR/EAS, but causal effects on disease may still differ
- Zhan 2025 AD: 5 protein→AD effects in EUR, zero in AFR, but 15× power differential makes this inconclusive
- Zhao 2022 GBMI: The 89/7/12 EUR-specific/trans-ancestry/AFR-specific split is the strongest systematic evidence for widespread non-transportability in protein→disease MR. Drug target validation (ACE→COPD in AFR, fosinopril) directly shows clinical value. Sex-specific opposite effects (ERAP1→IPF, NQO1→HF in males vs females) extend transportability framework beyond ancestry.

**NEW pairs available from newly found papers** (~29 additional):
- CETP drug-target MR (Dunca 2024): 7 pairs (4 non-transport, 3 transport)
- Metabolic→psoriasis (Ogawa 2019): 7 usable pairs (1 transport, 1 non-transport, 5 borderline/null)
- SLE→female cancers (Zhu 2023): 3 pairs (2 non-transport, 1 null transport)
- Neutrophil→lung cancer (Ren 2025): 1 borderline non-transport
- Urate→kidney function (Wu 2023): 2 non-transport (replaces misidentified urate→gout)
- IL6R→phenotypes (Wang 2022): 3 non-transport (T2D, glaucoma, WBC)
- BMI→gastric cancer (Park 2023): 1 non-transport (linear vs U-shaped)
- Coffee→eGFR (Yoo 2024): 1 transport (unit caveats)
- GBMI proteome MR (Zhao 2022): 3 transport (SERPINE2/ABO→VTE, ACE→COPD) + 1+ non-transport (SERPINF1→Stroke, plus up to ~100 from supplementary)
See SESSION_FINDINGS_SUMMARY.md for all details.

## Impact on paper claims

### With Tier 1 only (minimal effort, literature extraction):
- 12 original pairs with real published data + ~25 new pairs = ~37 real-data pairs
- 6 already-exact pairs preserved
- Remaining 53 original pairs: reframed as "domain-knowledge positive controls"
- Paper headline shifts from "44 transport pairs with circular Q" to "37+ pairs with published per-ancestry MR, independently validated"

### Recommended approach (Tier 1 first, Tier 2 selective):
1. Swap in all 12 Tier 1 pairs (literature extraction)
2. Add highest-quality new pairs (CETP, SLE, psoriasis — all proper trans-ethnic MR papers)
3. Run MR for highest-priority Tier 2 pairs:
   - T2DGGI T2D (WHR_T2D, fasting_glucose_T2D — BMI_T2D now Tier 1)
   - Wang 2023 VitD (vitD_MS, vitD_RA, vitD_AD — upgrades 3 pairs across 3 domains)
   - CRP 2025 (CRP_depression, CRP_RA, CRP_AD — upgrades 3 pairs across 3 domains)
   - Asthma exac. with pre-computed Q (external validation showcase)
4. Pre-register analysis plan with SHA before running any pipeline
   - PRACTICAL prostate cancer
   - Pancreatic MEC (resolves "uncorrectable false negative")
   - Telomere 2024 (resolves other false negative)
3. Mark Tier 3 as "domain-knowledge classification" in paper
4. Report two accuracy numbers: "real-data subset" and "full catalog"

## alcohol_CAD_MR reclassification

Real MVP data shows EUR/AFR/HISP all near OR=1.0 (homogeneous null).
Our catalog labels it non-transport based on Holmes 2014 vs Millwood 2019 comparison,
but these use different instruments, outcomes, and scales.
Options:
- Reclassify as transport (real data is homogeneous)
- Drop it (instruments not comparable across ancestries)
- Keep as-is but note the discrepancy

## Key consortium download links

| Source | URL | Notes |
|--------|-----|-------|
| GLGC 2021 | https://csg.sph.umich.edu/willer/public/glgc-lipids2021/ | 5 ancestry lipid GWAS |
| T2DGGI | http://www.diagram-consortium.org/downloads.html | 5 ancestry T2D |
| PGC | https://pgc.unc.edu/for-researchers/download-results/ | Ancestry-specific psych |
| CKDGen | https://ckdgen.imbi.uni-freiburg.de/ | Trans-ethnic CKD |
| Asthma exac. | https://zenodo.org/records/5513443 | Pre-computed Cochran's Q |
| PD multi-anc | Google Drive link in medrxiv 2022.08.04.22278432 | 4 ancestries, no application |
| PRACTICAL | AACRJ NG03 | 4 ancestry prostate cancer |
| Depression 2025 | doi:10.1038/s41562-024-02073-6 | Cross-ancestry MDD |
| IL6R MVP | medrxiv 2022.09.24.22280325 | AFR vs EUR explicit strata |
| Pancreatic MEC | PMID 32958499 | 5-ancestry per-ancestry ORs, het p=0.12 |
| Wang 2023 VitD | cnsgenomics.com/data/wang_2023/ | Per-ancestry files AFR/EAS/SAS |
| CRP 2025 | doi:10.1038/s41467-025-59155-w | 513K genomes, ancestry-specific |
| CRP 2014 | PMID 24622110 | Multi-ancestry AFR/HISP replication |
| Telomere 2024 | PMID 38789417 | 211K multi-ancestry meta-analysis |
| MVP suppl. | kp4cd.org/sites/default/files/.../MVP_GWAS_supplementary_tables_06-01-2022.xlsx | Check for bladder cancer, COPD |
| Hemani 2025 CAMeRa | doi:10.21203/rs.3.rs-6091701/v1 | Cross-ancestry MR framework, BMI→T2D Q p=0.002 |
| CETP EAS vs EUR | doi:10.1038/s41467-024-49109-z | 32 outcomes, asthma/lung cancer/CKD discordant |
| Zhao 2022 GBMI proteome MR | doi:10.1016/j.xgen.2022.100195 + epigraphdb.org/multi-ancestry-pwmr | Tables S7/S8/S16 have all per-ancestry ORs |

---

## NEW PAIR CANDIDATES from verified papers

### From CETP drug-target MR (Dunca 2024 Nat Commun, PMC11192935)
All Tier 1 — exact per-ancestry ORs with CIs from Figures 3-4 of the paper.
Caveat: exposure is CETP activity proxied via HDL-C (drug-target MR), not generic HDL-C.

| Pair candidate | Expected class | EUR OR (95% CI) | EAS OR (95% CI) | Interaction p | Notes |
|---------------|----------------|-----------------|-----------------|---------------|-------|
| CETP_asthma_MR | non-transport | 0.95 (0.91, 0.99) | 1.26 (1.16, 1.36) | 3.3×10⁻¹⁰ | Strongest discordance. EUR protective, EAS harmful |
| CETP_lung_cancer_MR | non-transport | 1.04 (0.99, 1.09) | 0.77 (0.70, 0.85) | 5.8×10⁻⁸ | EUR null, EAS protective |
| CETP_CKD_MR | non-transport | 0.93 (0.90, 0.97) | 1.31 (1.05, 1.63) | 2.8×10⁻³ | EUR protective, EAS harmful |
| CETP_breast_cancer_MR | non-transport | 1.07 (1.01, 1.13) | 0.92 (0.83, 1.00) | 6.7×10⁻³ | EUR harmful, EAS protective |
| CETP_PAD_MR | non-transport | 0.96 (0.87, 1.05) | 0.86 (0.84, 0.89) | 5.7×10⁻⁴ | EAS stronger |
| CETP_CHD_MR | transport | 0.95 (0.92, 0.99) | 0.89 (0.84, 0.94) | 5.2×10⁻² | Both protective |
| CETP_angina_MR | transport | 0.86 (0.84, 0.89) | 0.91 (0.84, 0.99) | 2.7×10⁻¹ | Both protective |
| CETP_HF_MR | transport | 0.89 (0.86, 0.93) | 0.85 (0.78, 0.94) | 4.4×10⁻¹ | Both protective |
| CETP_ICH_MR | transport | 0.75 (0.66, 0.85) | 0.69 (0.55, 0.87) | 5.9×10⁻¹ | Both protective |
| CETP_pneumonia_MR | transport | 0.87 (0.84, 0.90) | 0.89 (0.81, 0.99) | 5.3×10⁻¹ | Both protective |

### From Hemani 2025 (CAMeRa framework)
BMI→T2D is the only significant heterogeneity from 40 well-conducted EUR×EAS analyses.

| Pair candidate | Expected class | EUR logOR (SE) | EAS logOR (SE) | Q p-value | Notes |
|---------------|----------------|----------------|----------------|-----------|-------|
| BMI_T2D_MR (Hemani) | non-transport | 0.99 (0.07) | 0.66 (0.08) | 0.002 | Confirms non-transport with proper FEMA instruments |
| LDL_stroke_large_artery | transport | — | — | >0.05 | Homogeneous across all 5 ancestries; logOR=0.29 (0.05) |

### From Bejar 2021 (VitD → T2D)
Borderline candidate. South Asian vs European (not East Asian).

| Pair candidate | Expected class | SA META OR (95% CI) | EUR cohorts | Notes |
|---------------|----------------|---------------------|-------------|-------|
| VitD_T2D_MR | borderline non-transport | 1.003 (1.00–1.01), p=0.029 | all ~1.00, p>0.6 | Very small effect sizes. DHCR7 instrument: OR=1.05 (1.0–1.11) overall |

### From Ren et al. 2025 (Neutrophil → Lung Cancer, J Cancer, PMC11660127)
VERIFIED from Table 1. Two-sample bidirectional MR in EUR and EAS.

| Pair candidate | Expected class | EUR beta (SE), OR | EAS beta (SE), OR | Notes |
|---------------|----------------|-------------------|-------------------|-------|
| neutrophil_lung_cancer_MR | borderline non-transport | 0.027 (0.011), OR=1.027 p=0.017 | 0.201 (0.103), OR=1.223 p=0.052 | Same direction, 7.4x magnitude difference. Q p=0.093 |

### From Ogawa et al. 2019 (Metabolic traits → Psoriasis, J Invest Dermatol, PMC7028352)
VERIFIED from Table 1 and Figure 1. Trans-ethnic MR with 9 exposures in EUR and JPN.
Caveat: JPN sample very small (282 cases, 426 controls); different phenotype normalization.

| Pair candidate | Expected class | EUR IVW β (SE) | JPN IVW β (SE) | Notes |
|---------------|----------------|----------------|----------------|-------|
| BMI_psoriasis_MR | transport | 0.464 (0.112) p=3.1e-5 | 1.275 (0.472) p=0.007 | Both positive. JPN 2.7x larger |
| blood_sugar_psoriasis_MR | non-transport | -0.537 (0.269) | 0.235 (0.671) | OPPOSITE signs! EUR protective, JPN harmful |
| triglycerides_psoriasis_MR | transport (null) | 0.085 (0.088) | 0.139 (0.369) | Both null |
| total_chol_psoriasis_MR | non-transport | 0.054 (0.063) | -0.595 (0.476) | Opposite signs, both null |
| LDL_psoriasis_MR | non-transport | 0.051 (0.054) | -0.300 (0.385) | Opposite signs, both null |
| HDL_psoriasis_MR | transport (null) | -0.026 (0.072) | -0.048 (0.509) | Both null |
| HbA1c_psoriasis_MR | transport (null) | -0.143 (0.273) | -0.289 (0.477) | Both null, same direction |
| SBP_psoriasis_MR | non-transport | 0.006 (0.010) | 1.080 (0.781) | Massive magnitude difference |
| DBP_psoriasis_MR | non-transport | 0.017 (0.017) | 1.010 (0.963) | Massive magnitude difference |

### From Zhu et al. 2023 (SLE → Female Cancers, Chinese Med J)
VERIFIED from Figures 2 and 4. Trans-ethnic MR in EUR and EAS. Proper two-sample MR.

| Pair candidate | Expected class | EUR IVW OR (95% CI) | EAS IVW OR (95% CI) | Notes |
|---------------|----------------|---------------------|---------------------|-------|
| SLE_endometrial_cancer_MR | non-transport | 0.961 (0.935–0.987) p=0.004 | 0.992 (0.924–1.065) p=0.819 | EUR significant, EAS null |
| SLE_breast_cancer_MR | non-transport | 0.989 (0.974–1.005) p=0.171 | 0.951 (0.918–0.986) p=0.006 | EUR null, EAS significant |
| SLE_ovarian_cancer_MR | transport (null) | 0.996 (0.980–1.012) p=0.632 | 1.030 (0.947–1.119) p=0.491 | Both null |

### From Bogumil 2020 (PRS → Pancreatic Cancer, MEC, PMID 32958499)
VERIFIED per-ancestry PRS ORs, but this is PRS (not two-sample MR). Useful for Discussion only.

| Ancestry | PRS OR (per IQR) | 95% CI | Notes |
|----------|------------------|--------|-------|
| African American | 1.91 | 1.55–2.35 | |
| White | 1.85 | 1.38–2.46 | |
| Latino | 1.65 | 1.26–2.17 | |
| Japanese American | 1.46 | 1.19–1.79 | |
| Native Hawaiian | ~1.33 | NS | |
| P_heterogeneity = 0.12 (modest) | | | |

### From Zhao 2022 (GBMI Proteome-wide MR, Cell Genomics 2:100195)
VERIFIED from main text. Full per-ancestry ORs for 108 signals in supplementary Tables S7/S8/S16.
Main text provides exact ORs for key pairs below. Proteome-wide MR using cis-pQTLs as instruments.

| Pair candidate | Expected class | EUR OR (95% CI) | AFR OR (95% CI) | Notes |
|---------------|----------------|-----------------|-----------------|-------|
| SERPINE2_VTE_proteome_MR | transport | 0.94 (0.92, 0.96) | 0.82 (0.67, 0.95) | Both protective. Q=2.32, p=0.128. Coloc 99%/100% |
| ABO_VTE_proteome_MR | transport | 1.11 | 1.33 | Both risk. CIs in supplementary. LD r²=1.0/0.80 |
| ACE_COPD_proteome_MR | transport | significant (suppl) | 0.88 (0.81, 0.95) | Fosinopril validated in AFR. Phase 4 trial NCT01014338 |
| SERPINF1_stroke_proteome_MR | non-transport | p=0.83 (null) | p=3.76x10⁻⁵ (significant) | AFR-specific. Novel protein-disease pair |

Additionally: 89 EUR-specific signals, 12 AFR-specific signals in supplementary tables.
Extracting Tables S7/S8/S16 would yield up to ~100 more Tier 1 pairs (most EUR-specific due to power).

### Updated Grand Summary of NEW Tier 1 candidates

| Source | Transport pairs | Non-transport pairs | Total new |
|--------|----------------|--------------------|----|
| CETP Nat Commun 2024 | 5 (CHD, angina, HF, ICH, pneumonia) | 5 (asthma, lung ca, CKD, breast ca, PAD) | 10 |
| Neutrophil→lung cancer 2025 | 0 | 1 (borderline) | 1 |
| Psoriasis trans-ethnic 2019 | 1 (BMI) + 3 nulls | 4 (blood sugar, chol, BP) | 8 |
| SLE→female cancers 2023 | 1 (ovarian, null) | 2 (endometrial, breast) | 3 |
| CAMeRa BMI→T2D 2025 | 0 | 1 | 1 |
| GBMI proteome MR (Zhao 2022) | 3 (SERPINE2/ABO/ACE) | 1+ (SERPINF1; up to ~100 in suppl) | 4+ (main text) |
| **TOTAL NEW** | **~13** | **~14+** | **~27+** |

Combined with 12 existing Tier 1 + 6 already-exact = potentially **45+ pairs with verified real data** (original 18 + 27 new). If Zhao 2022 supplementary tables are extracted, this could reach 100+ pairs with real per-ancestry data.
