# Session Findings Summary: Paper Search & Verification

## Papers Read and Verified This Session

| # | Paper | File | What it is | Per-ancestry MR? | Verdict |
|---|-------|------|-----------|-----------------|---------|
| 1 | Kember 2024 (MVP Alcohol) | mvp_2024_alcohol_real.pdf | One-sample MR ADH1B→CHD in 3 ancestries | YES (EUR/AFR/HISP) | Tier 1: all null, TRANSPORT |
| 2 | Wang 2022 (IL6R MVP) | il6r_mvp_preprint_real.pdf | PheWAS rs2228145 in AFR vs EUR | YES (drug-target cis-MR) | Tier 1: CVD transport, T2D non-transport |
| 3 | Wu 2023 (Urate kidney) | heliyon_2023_urate_real.pdf | Urate↔kidney function, 3 ancestries | YES (EUR/AFR/Asian) | WRONG OUTCOME for urate_gout; new pairs possible |
| 4 | Dunca 2024 (CETP) | cetp_eas_eur.pdf + XML | Drug-target MR CETP, 32 outcomes | YES (EUR/EAS, interaction p) | GOLDMINE: 4 non-transport + 6 transport pairs |
| 5 | Ren 2025 (Neutrophil lung) | neutrophil_lung_cancer.xml | Two-sample MR NC→LC | YES (EUR/EAS) | Tier 1: borderline non-transport |
| 6 | Bejar 2021 (VitD T2D) | vitd_t2d_bidirectional.pdf + XML | Bidirectional MR VitD↔T2D | POOLED only | REJECTED: composite null, no per-ancestry split |
| 7 | Ogawa 2019 (Obesity psoriasis) | obesity_psoriasis_real.pdf | Trans-ethnic MR 9 traits→psoriasis | YES (EUR/JPN betas+SEs) | GOLDMINE: 9 pairs with exact numbers |
| 8 | Zhu 2023 (SLE cancer) | sle_cancer_transethnic_real.pdf | Trans-ethnic MR SLE→3 cancers | YES (EUR/EAS ORs) | 3 pairs: endometrial + breast non-transport |
| 9 | Kim 2022 (PD multi-ancestry) | pd_multiancestry_real.pdf | Multi-ancestry GWAS | NO (GWAS, not MR) | Tier 2 outcome source only |
| 10 | Hemani 2025 (CAMeRa) | ldl_stroke_2025_methods.pdf | Cross-ancestry MR framework | YES (40 EUR×EAS pairs) | KEY: BMI→T2D Q p=0.002, method validation |
| 11 | Park 2023 (BMI gastric) | HTML verified | Ethnic-specific MR BMI→GC | YES (EUR/Korean) | EUR linear vs Korean U-shaped |
| 12 | Yoo 2024 (Coffee kidney) | coffee_kidney_europepmc.xml | Coffee→eGFR EUR vs EAS | YES (but different units) | Transport (same direction), unit harmonization needed |
| 13 | Su 2022 (Smoking SCZ EAS) | web search verified | Smoking→SCZ in East Asia | YES (EAS/EUR ORs) | Tier 1 upgrade for smoking_schizophrenia_MR |

## Corrections Made to REPLACEMENT_PLAN.md

1. **urate_gout_MR**: Reverted Tier 1 → Tier 2. Heliyon paper is urate→kidney function, NOT urate→gout.
2. **IL6R_CAD_MR**: Re-verified as Tier 1 from real PDF. CVD outcomes concordant across AFR/EUR.
3. **IL6R_RA_MR**: Stays Tier 3. RA not among 29 heterogeneous traits in IL6R PheWAS.
4. **O'Loughlin citation**: Fixed "Cheng 2023" → "O'Loughlin 2023" (BMI→depression EAS).
5. **Pancreatic MEC**: Confirmed as PRS/GRS study, NOT insulin resistance MR. Numbers verified but wrong study type.
6. **Telomere 2024**: Confirmed as GWAS validation study, NOT MR-on-cancer.

## Existing Pairs: Tier Upgrades

| Pair | Old Tier | New Tier | Source | Key Numbers |
|------|----------|----------|--------|-------------|
| IL6R_CAD_MR (#14) | 3 (dead link) | **1** | IL6R MVP PheWAS (real PDF verified) | EUR IHD OR=0.96, AFR OR=0.99 |
| smoking_schizophrenia_MR (#32) | 2 | **1** | Su 2022 PMC9463183 | EAS OR=4.00 (0.89-18.01), EUR OR=1.53 |
| BMI_T2D_MR (#8) | 2 | **1** (from CAMeRa) | Hemani 2025 preprint | EAS logOR=0.66, EUR logOR=0.99, Q p=0.002 |
| LDL_stroke_MR (#12) | 2 | **1** (from CAMeRa) | Hemani 2025 preprint | Large artery: homogeneous; any-stroke: Q p=0.041 |

## NEW Pairs: From Newly Found Papers

### CETP Drug-Target MR (Dunca 2024, Nature Communications)
All per SD HDL-C increase (CETP inhibition proxy). EUR vs EAS.

| New Pair | Classification | EUR OR (95% CI) | EAS OR (95% CI) | Interaction p |
|----------|---------------|-----------------|-----------------|---------------|
| CETP_asthma_MR | **NON-TRANSPORT** | 0.95 (0.91-0.99) | 1.26 (1.16-1.36) | 3.3e-10 |
| CETP_lung_cancer_MR | **NON-TRANSPORT** | 1.04 (0.99-1.09) | 0.77 (0.70-0.85) | 5.8e-8 |
| CETP_CKD_MR | **NON-TRANSPORT** | 0.93 (0.90-0.97) | 1.31 (1.05-1.63) | 2.8e-3 |
| CETP_breast_cancer_MR | **NON-TRANSPORT** | 1.07 (1.01-1.13) | 0.92 (0.83-1.00) | 6.7e-3 |
| CETP_CHD_MR | TRANSPORT | 0.95 (0.92-0.99) | 0.89 (0.84-0.94) | 5.2e-2 |
| CETP_HF_MR | TRANSPORT | 0.89 (0.86-0.93) | 0.85 (0.78-0.94) | 4.4e-1 |
| CETP_pneumonia_MR | TRANSPORT | 0.87 (0.84-0.90) | 0.89 (0.81-0.99) | 5.3e-1 |

**Caveat**: Drug-target MR, not standard 2-sample. Exposure is pharmacological CETP inhibition.

### Obesity/Metabolic → Psoriasis (Ogawa 2019, J Invest Dermatol)
EUR vs JPN, IVW betas and SEs.

| New Pair | Classification | EUR β (SE) | JPN β (SE) | Notes |
|----------|---------------|-----------|-----------|-------|
| BMI_psoriasis_MR | **TRANSPORT** | 0.464 (0.112) | 1.275 (0.472) | Both positive; JPN 2.7× larger |
| blood_sugar_psoriasis_MR | **NON-TRANSPORT** | -0.537 (0.269) | 0.235 (0.671) | Opposite signs |
| total_chol_psoriasis_MR | borderline | 0.054 (0.063) | -0.595 (0.476) | Opposite but JPN nonsig |
| triglycerides_psoriasis_MR | TRANSPORT (null) | 0.085 (0.088) | 0.139 (0.369) | Both null |
| HDL_psoriasis_MR | TRANSPORT (null) | -0.026 (0.072) | -0.048 (0.509) | Both null |
| LDL_psoriasis_MR | borderline | 0.051 (0.054) | -0.300 (0.385) | Opposite but JPN nonsig |
| HbA1c_psoriasis_MR | TRANSPORT (null) | -0.143 (0.273) | -0.289 (0.477) | Both null |
| SBP_psoriasis_MR | underpowered | 0.006 (0.010) | 1.080 (0.781) | JPN massive SE |
| DBP_psoriasis_MR | underpowered | 0.017 (0.017) | 1.010 (0.963) | JPN massive SE |

**Caveat**: JPN sample small (282 cases). Different GWAS phenotype normalization.

### SLE → Female Cancers (Zhu 2023, Chinese Medical Journal)
EUR vs EAS, IVW ORs.

| New Pair | Classification | EUR OR (95% CI) | EAS OR (95% CI) |
|----------|---------------|-----------------|-----------------|
| SLE_endometrial_cancer_MR | **NON-TRANSPORT** | 0.961 (0.935-0.987) p=0.004 | 0.992 (0.924-1.065) p=0.82 |
| SLE_breast_cancer_MR | **NON-TRANSPORT** | 0.989 (0.974-1.005) p=0.17 | 0.951 (0.918-0.986) p=0.006 |
| SLE_ovarian_cancer_MR | TRANSPORT (null) | 0.996 (0.980-1.012) p=0.63 | 1.030 (0.947-1.119) p=0.49 |

### Neutrophil → Lung Cancer (Ren 2025, J Cancer)
| New Pair | Classification | EUR (β, SE) | EAS (β, SE) |
|----------|---------------|-------------|-------------|
| neutrophil_lung_cancer_MR | **borderline NON-TRANSPORT** | 0.027, 0.011 (p=0.017) | 0.201, 0.103 (p=0.052) |

Q = 2.83, p = 0.093. Effect 7.4× larger in EAS but same direction.

### Urate → Kidney Function (Wu 2023, Heliyon)
Three-ancestry data that could replace the misidentified urate_gout_MR pair.

| New Pair | Classification | EUR β | AFR β | Asian β |
|----------|---------------|-------|-------|---------|
| urate_BUN_MR | **NON-TRANSPORT** | 0.036 (p=0.03) | 0.223 (p<0.001) | -0.015 (p=0.28) |
| urate_eGFR_MR | **NON-TRANSPORT** | -0.011 (p=0.10) | 0.007 (p=0.55) | -0.112 (p<0.001) |
| urate_CKD_MR | TRANSPORT? | EUR OR=1.18 (p=0.02) | not reported | not reported |

### IL6R → Specific Phenotypes (Wang 2022, MVP PheWAS)
Potential new pairs from verified heterogeneous associations.

| New Pair | Classification | EUR OR | AFR OR | het p |
|----------|---------------|--------|--------|-------|
| IL6R_T2D_MR | **NON-TRANSPORT** | 1.001 | 0.956 (p=9e-4) | 0.085 |
| IL6R_glaucoma_MR | **NON-TRANSPORT** | 1.012 | 0.911 (p=1.4e-5) | 3.2e-4 |
| IL6R_WBC_MR | **NON-TRANSPORT** | 1.015 | 1.207 (p=6.5e-7) | 3.1e-3 |

### BMI → Gastric Cancer (Park 2023, Gastric Cancer)
| New Pair | Classification | EUR | Korean |
|----------|---------------|-----|--------|
| BMI_gastric_cancer_MR | **NON-TRANSPORT** | OR=1.17 (1.01-1.36) linear | No linear effect; U-shaped |

**Caveat**: Qualitative dose-response difference (linear vs U-shaped). Interesting Discussion point about limitations of linear Q-test.

### Proteome-wide MR (Zhao 2022, Cell Genomics — GBMI)
Multi-ancestry proteome-wide MR: 1,310 proteins EUR, 1,311 proteins AFR, 8 diseases.

| New Pair | Classification | EUR | AFR | Notes |
|----------|---------------|-----|-----|-------|
| SERPINE2_VTE_proteome_MR | **TRANSPORT** | OR=0.94 (0.92-0.96) | OR=0.82 (0.67-0.95) | Same direction, Q=2.32 p=0.128 |
| ABO_VTE_proteome_MR | **TRANSPORT** | OR=1.11 | OR=1.33 | Same direction, CIs in supplementary |
| ACE_COPD_proteome_MR | **TRANSPORT** | significant (suppl) | OR=0.88 (0.81-0.95) | Validated in AFR; fosinopril drug target |
| SERPINF1_stroke_proteome_MR | **NON-TRANSPORT** | p=0.83 (null) | p=3.76x10^-5 | AFR-specific signal |

Plus 89 EUR-specific + 12 AFR-specific signals in supplementary tables (potential ~100 additional pairs if extracted).

**Sex-specific non-transportability from same paper (Figure 2):**
| Protein → Disease | Female | Male | Pattern |
|-------------------|--------|------|---------|
| IL-17RA → Asthma | OR=1.00 (null) | OR=1.03 (p=1.69x10^-9) | Male-specific |
| ERAP1 → IPF | OR=1.08 (risk) | OR=0.96 (protective) | OPPOSITE |
| NQO1 → HF | OR=0.87 (protective) | OR=1.38 (risk) | OPPOSITE |

### Coffee → eGFR (Yoo 2024)
| New Pair | Classification | EUR β | EAS β |
|----------|---------------|-------|-------|
| coffee_eGFR_MR | TRANSPORT (same direction) | 0.052 (per cup/day) | 0.077 (per cup/week) |

**Caveat**: Exposure units differ. Direct beta comparison requires harmonization. High within-ancestry IV heterogeneity in EUR (Q=140.4).

---

## Updated Tier Counts (Existing 71 Pairs)

| Tier | Before | After | Change |
|------|--------|-------|--------|
| Tier 1 | 9 | **12** | +3 (IL6R_CAD re-verified, smoking_SCZ, BMI_T2D from CAMeRa) |
| Tier 2 | 33 | **30** | -3 (upgrades to Tier 1) |
| Tier 3 | 23 | **23** | unchanged |
| Already exact | 6 | **6** | unchanged |

## New Pairs Available (Not in Original 71)

| Source Paper | Transport pairs | Non-transport pairs | Total new |
|-------------|----------------|--------------------|----|
| CETP (Dunca 2024) | 3 | 4 | **7** |
| Psoriasis (Ogawa 2019) | 4 (incl null) | 1 confirmed + 2 borderline | **7** (usable) |
| SLE cancer (Zhu 2023) | 1 | 2 | **3** |
| Neutrophil lung (Ren 2025) | 0 | 1 | **1** |
| Urate kidney (Wu 2023) | 0 | 2 | **2** |
| IL6R phenotypes (Wang 2022) | 0 | 3 | **3** |
| BMI gastric (Park 2023) | 0 | 1 | **1** |
| Coffee eGFR (Yoo 2024) | 0-1 | 0 | **1** |
| GBMI proteome MR (Zhao 2022) | 3 (SERPINE2/ABO/ACE) | 1+ (SERPINF1 + 89 EUR-specific) | **4+ main text** |
| **TOTAL NEW** | **11-12** | **14-15+** | **~29+** |

## Grand Total After This Session

**71 original + ~29 new = ~100 pairs**, with **12 + ~23 = ~35 having real Tier 1 data** (published per-ancestry MR estimates). Zhao 2022 supplementary tables (S7/S8/S16) contain per-ancestry ORs for up to 108 signals — extracting these could dramatically expand the Tier 1 count.

## Continuation Session (2026-07-17): Additional Papers Read

| # | Paper | Per-ancestry MR? | Verdict |
|---|-------|-----------------|---------|
| 14 | Tyrrell 2019 (BMI → depression) | EUR only (UK Biobank) | OR=1.18 (1.09-1.28). Swap script has WRONG OR=1.08. Must fix |
| 15 | Johnson 2024 (SCZ/cannabis cross-ancestry) | EUR only (AFR underpowered) | CANNOT upgrade cannabis→SCZ. MR was EUR-only |
| 16 | Park 2023 (BMI → gastric cancer) | YES (EUR + Korean) | EUR IVW OR=1.10; Korean OR=1.00. Nonlinear U-shaped in Korean |
| 17 | Cho 2024 (urate mega-GWAS) | POOLED only | N=1M GWAS, MR not per-ancestry. Tier 2 GWAS source |
| 18 | Wang 2023 (PRACTICAL prostate) | NO (GWAS/GRS only) | Per-ancestry GRS ORs but NO exposure→cancer MR |
| 19 | Li 2025 (breast cancer multi-ancestry) | NO (GWAS only) | Heritability + genetic correlations, no MR |
| 20 | Smith 2023 (T2DGGI subtypes) | NO (clustering) | 12 T2D genetic clusters. Discussion context for BMI→T2D non-transport |
| 21 | Zhan 2025 (AD proteomics MR) | YES (EUR → AFR attempt) | 5 proteins causal in EUR, zero in AFR. But 15× power deficit |
| 22 | Su 2022 page 6 (back matter) | N/A | No additional data beyond pages 1-5 |
| 23 | Zhao 2022 (GBMI proteome-wide MR) | YES (EUR + AFR per-ancestry) | **GOLDMINE**: 45 EUR + 7 AFR MR signals. 7 trans-ancestry, 89 EUR-specific, 12 AFR-specific. SERPINE2→VTE exact ORs. ACE→COPD validated in AFR |
| 24 | Wootton 2020 (Smoking → depression/SCZ) | YES (EUR IVW with CI) | Smoking init→SCZ: OR=1.53 (1.35-1.74). Lifetime smoking: OR=2.27 (1.67-3.08). Matches Su 2022 EUR citation exactly |
| 25 | Ooi 2019 (BMI → breast cancer EUR) | YES (EUR BCAC) | IVW OR=0.81 (0.74-0.89), 228,951 participants. Protective direction |
| 26 | Wu 2025 (BMI PheWAS EAS) | YES (EAS 159 outcomes) | BMI→breast cancer OR=0.67 (0.53-0.84). Also prostate OR=0.66 (0.53-0.81) |
| 27 | Austin-Zimmerman 2026 (CUD↔psychosis) | POOLED (cross-ancestry GWAS input) | CUD→psychosis β=0.31 (0.22-0.41). Uses multi-ancestry CUD GWAS but MR appears pooled, not per-ancestry. Need supplement |

### Key corrections from continuation session
1. **Tyrrell 2019 OR discrepancy**: OR = 1.18, NOT 1.08. Error in swap script must be fixed
2. **Johnson 2024 ruled out**: Cannabis→SCZ stays Tier 2 (no AFR MR data exists)
3. **PRACTICAL prostate ruled out**: Not an MR paper. Height→prostate stays Tier 2/3
4. **Breast cancer ruled out**: Not an MR paper
5. **Park 2023 exact data extracted**: BMI→gastric cancer has exact EUR + Korean ORs now

## Continuation Session (2026-07-17, part 2): Supplement Checks & Mason Review

| # | Paper | Per-ancestry MR? | Verdict |
|---|-------|-----------------|---------|
| 28 | Austin-Zimmerman 2026 supplement (mmc2.xlsx, 24 sheets) | NO — MR-CLUST only, no per-ancestry stratification | cannabis→SCZ stays Tier 2 |
| 29 | Cho 2024 supplement (ST1-ST28) | POOLED — ST25 has SU→gout OR=4.86 but no ancestry column | urate→gout stays Tier 2 |
| 30 | Mason et al. 2025 (arXiv:2510.17554v1) | N/A (review paper) | Key methodological citation for Discussion. 6 pathways for cross-ancestry heterogeneity; only 1 is real biology. Full quotes saved in MASON_2025_KEY_QUOTES.md |

### Key resolutions
1. **Both Tier 1 pending pairs resolved**: cannabis→SCZ and urate→gout both stay Tier 2.
2. **Mason et al. 2025**: Independent authority (Hemani + Burgess + 14 co-authors) supporting composite-hypothesis framing. "Evidence beyond MR is essential before concluding that causal effects vary between ancestry populations."
3. **Pre-registration updated**: PREREGISTRATION_batch3.md section 2 now reflects resolved status
4. **CAMeRa BMI→T2D extracted**: EUR logOR=0.99 (SE=0.07), EAS logOR=0.66 (SE=0.08), Q p=0.002. Added to swap script as pair #12. Text on p8 of Hemani 2025 provides exact numbers
5. **CAMeRa LDL→stroke EXTRACTED**: Per-ancestry estimates obtained from analysis repo (github.com/yoonsucho/camera_analysis) rendered HTML kable tables. EUR logOR=0.0811 (SE=0.0185), EAS=0.0221 (0.0272), AFR=0.2852 (0.0826), AMR=0.3016 (0.2049), SAS=0.2061 (0.1778). 5-ancestry Q=12.09 (p=0.017, non-transport). EUR-vs-EAS only Q=3.21 (p=0.073, transport). Added to swap script.
6. **IL6R_CAD_MR added to swap script**: EUR IHD OR=0.96 (0.95-0.97), AFR OR=0.99 (0.95-1.02). Was Tier 1 since earlier session but not yet in swap script. Now pair #13 in REPLACEMENTS dict. Computed: EUR beta=-0.0408 (SE=0.0053), AFR beta=-0.0101 (SE=0.0181)
7. **Total swap script pairs: 14** (13 in REPLACEMENTS + alcohol_CAD_MR handled separately). All 14 Tier 1 pairs now in swap script. No pairs pending.

## Still Needs Extraction

1. ~~**Mullins 2024** — Cross-ancestry SCZ/cannabis/smoking MR~~ → RESOLVED: Johnson 2024 IS this paper. MR is EUR-only. Dead end.
2. **T2DGGI supplementary materials** — May contain per-ancestry MR tables. But main text (Smith 2023) is a subtyping paper, not MR.
3. ~~**Su 2022 full text**~~ → RESOLVED: Wootton 2020 (PMC7610182, Psychol Med) fetched. Smoking initiation → SCZ EUR IVW OR=1.53 (1.35-1.74), p=3.7e-11. Also available: lifetime smoking index OR=2.27 (1.67-3.08). Added to swap script.
4. ~~**BMI gastric cancer full tables**~~ → RESOLVED: Park 2023 exact ORs extracted (EUR IVW 1.10, Korean IVW 1.00)
5. ~~**Cell Press zip** (GBMI proteome-wide MR)~~ → RESOLVED: Zhao 2022 Cell Genomics. GOLDMINE — 7 trans-ancestry + 89 EUR-specific + 12 AFR-specific signals. Per-ancestry ORs for SERPINE2→VTE, ABO→VTE, ACE→COPD. Full data in Tables S7/S8/S16.
6. ~~**Fix swap script**~~ → DONE: Tyrrell 2019 OR fixed (1.08→1.18). Wootton 2020 smoking→SCZ EUR added (OR=1.53, CI 1.35-1.74)
7. **Zhao 2022 supplementary tables** — Tables S7, S8, S16 have full per-ancestry ORs for all 108 signals. Would yield many more Tier 1 pairs if downloaded

## Key Methodological Papers for Citation

1. **Hemani 2025 CAMeRa** — Cross-ancestry MR framework. Uses Cochran's Q exactly as we do. Shows most apparent heterogeneity is artifactual (LD, weak instruments). Should cite as independent validation.
2. **Dunca 2024 CETP** — Drug-target MR comparing ancestries. Provides interaction p-values for each outcome. Model paper for our framework.
3. **Ogawa 2019 psoriasis** — "Trans-ethnic MR" in the title. Directly comparable to our approach.
4. **Smith 2023 T2DGGI** — Genetic subtypes explain ancestry-associated T2D risk differences (BMI=30 in EUR ≈ BMI=24.2 in EAS). Mechanistic context for BMI→T2D non-transportability.
5. **Cho 2024 urate GWAS** — ρ_gc=0.942 for SU genetics across EUR/EAS. Shared genetic architecture of EXPOSURE does not guarantee shared causal effects on OUTCOME — key conceptual point.
6. **Zhao 2022 GBMI proteome MR** — Systematic multi-ancestry proteome-wide MR across 8 diseases. The 89/7/12 EUR-specific/trans-ancestry/AFR-specific split is the strongest systematic evidence that protein→disease causal effects are largely ancestry-specific. Drug target validation (ACE→COPD in AFR) directly demonstrates clinical value of testing transportability. Sex-specific opposite effects (ERAP1→IPF, NQO1→HF) extend the framework.
