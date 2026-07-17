# Pre-registration: Real-Data Swap & Re-Validation (Batch 3 Expansion)

**Date:** 2026-07-17
**Author:** Elliot Tower
**Frozen at commit SHA:** 85de0af

**Freeze this before running `swap_tier1_real_data.py` against `pairs_curated.json`.**

---

## 1. What's being replaced and why

The original 71-pair catalog used hand-entered, rounded-to-2-decimal betas
for all 44 transport pairs. An internal audit found P(all 44 having Q<1
under true H0) ~ 10^-20 --- evidence of circularity, not a real result.
This pre-registration covers the swap-in of independently published,
per-ancestry MR/GWAS estimates to replace those hand-entered values, and
the re-run of the full 71-pair validation on the resulting mixed
real/domain-knowledge catalog.

---

## 2. Frozen inventory

### Tier 1 --- swap now (14 pairs in swap script, real data in hand)

| # | Pair ID | Source papers | EUR | EAS/AFR | Pre-computed Q |
|---|---------|--------------|-----|---------|---------------|
| 1 | LDL_CAD_MR | Wang 2022 | OR=1.82 | OR=1.77 (EAS) | Q=0.07, transport |
| 2 | HDL_CAD_MR | Wang 2022 | OR=0.89 | OR=0.89 (EAS) | Q~0, transport |
| 3 | triglycerides_CAD_MR | Wang 2022 | OR=1.27 | OR=1.44 (EAS) | Q=0.48, transport |
| 4 | SBP_CAD_MR | Wang 2022 | OR=1.96 | OR=1.68 (EAS) | Q=1.40, transport |
| 5 | T2D_CAD_MR | Wang 2022 | OR=1.08 | OR=1.13 (EAS) | Q=2.32, transport |
| 6 | BMI_CAD_MR | Wang 2022 | OR=1.38 | OR=1.67 (EAS) | Q=7.27, non-transport |
| 7 | Lp_a_CAD_MR | CKB Circ 2025 | RR=0.78 | RR=0.78 (EAS) | Q~0, transport |
| 8 | BMI_depression_MR | Tyrrell 2019 + O'Loughlin 2023 | OR=1.18 | OR=0.96 (EAS) | Q=36.4, non-transport |
| 9 | alcohol_CAD_MR | Kember 2024 MVP | OR=1.02 | OR=1.01 (AFR), 1.04 (HISP) | Q=0.71, transport |
| 10 | smoking_schizophrenia_MR | Wootton 2020 + Su 2022 | OR=1.53 | OR=4.00 (EAS, wide CI) | Q=1.56, transport |
| 11 | BMI_breast_cancer_MR | Ooi 2019 + Wu 2025 | OR=0.81 | OR=0.67 (EAS) | Q=2.25, transport |
| 12 | BMI_T2D_MR | Hemani 2025 CAMeRa | logOR=0.99/SD | logOR=0.66/SD (EAS) | Q p=0.002, non-transport |
| 13 | IL6R_CAD_MR | Wang 2022 IL6R MVP | OR=0.96 | OR=0.99 (AFR) | ~transport (both near null) |
| 14 | LDL_stroke_MR | Hemani 2025 CAMeRa repo | logOR=0.081 | 5 ancestries (see below) | Q=12.09 (5-anc), non-transport |

Pairs 9, 11, and 14 have methodological flags:
- **alcohol_CAD_MR**: Already marked for reclassification. Original non-transport
  label was based on incomparable instruments (Holmes 2014 EUR ADH1B vs
  Millwood 2019 EAS ADH1B/ALDH2). Real MVP data with consistent instruments
  shows homogeneous nulls. This is expected to flip.
- **BMI_breast_cancer_MR**: Assembled from two independent single-ancestry
  papers (Ooi 2019 EUR BCAC + Wu 2025 EAS PheWAS), not one multi-ancestry
  study. Flagged as "assembled" sub-category in all tables.
- **LDL_stroke_MR**: 5-ancestry pair (EUR/EAS/AFR/AMR/SAS) from CAMeRa
  analysis repo (github.com/yoonsucho/camera_analysis, mr.html kable output).
  Exact per-ancestry estimates extracted from rendered HTML tables:
  EUR logOR=0.0811 (SE=0.0185), EAS=0.0221 (0.0272), AFR=0.2852 (0.0826),
  AMR=0.3016 (0.2049), SAS=0.2061 (0.1778). Overall Q=12.09 (df=4, p=0.017,
  non-transport). EUR-vs-EAS only: Q=3.21 (p=0.073, transport). Heterogeneity
  driven by AFR (Qj=6.66, p=0.010). Results report BOTH: 5-ancestry Q as
  primary (matches paper's analysis), EUR-vs-EAS Q as sensitivity.

### Tier 1 --- pending supplement check (2 pairs) --- RESOLVED

Both pending pairs stay **Tier 2**. Supplements inspected 2026-07-17:

- **cannabis_schizophrenia_MR**: Austin-Zimmerman 2026 supplement
  inspected (mmc2.xlsx, 24 sheets). SD17-SD18 contain MR-CLUST
  (SNP-level clustering for pleiotropy detection) but NO per-ancestry
  MR stratification. The underlying MR uses pooled cross-ancestry CUD
  GWAS as exposure. **Verdict: stays Tier 2.**
- **urate_gout_MR**: Cho 2024 supplement inspected (ST1-ST28 of
  41467_2024_47805_MOESM4_ESM.xlsx). ST25 has MR for serum urate →
  gout (IVW OR=4.86, p=3e-36, 89 SNPs) but results are POOLED
  cross-ancestry with no ancestry column. **Verdict: stays Tier 2.**

**Final Tier 1 count: 14** (all in swap script --- 13 in REPLACEMENTS
dict + 1 alcohol_CAD_MR handled separately).
No further pairs pending. No supplement decisions pending.

### Tier 1 assembled --- pre-specified sub-category

BMI_breast_cancer_MR is assembled from two independent single-ancestry
MR papers. In all results tables, this pair will be:
- Flagged with an "A" superscript (assembled)
- Reported separately in sensitivity analysis (accuracy with/without)
- Methodologically noted in the paper's methods section

### Pre-specified sensitivity: LDL_stroke_MR ancestry-subset analysis

LDL_stroke_MR is the only Tier 1 pair with >2 ancestries (K=5: EUR,
EAS, AFR, AMR, SAS). The transport verdict depends on which ancestries
are compared:

- **5-ancestry Q=12.09, df=4, p=0.017**: non-transport
- **EUR-vs-EAS Q=3.21, df=1, p=0.073**: transport
- **Drop AFR (LOO): Q=5.20, df=3, p=0.156**: transport (FLIPS)
- **Drop EAS (LOO): Q=7.27, df=3, p=0.063**: transport (FLIPS)

AFR contributes 55% of total Q (Qj=6.66 of 12.09). The AFR estimate
(logOR=0.285, SE=0.083) is 3.5x the EUR estimate (0.081) with a CI
that excludes the EUR point estimate. This is either a genuine
ancestry-specific effect size (Mason pathway 5) or an artifact of
smaller AFR stroke GWAS samples and population-specific LD structure
(Mason pathways 1-4). CAMeRa's FEMA instrument selection mitigates
some LD artifacts but cannot fully resolve this.

Full LOO and pairwise results: `LDL_STROKE_LOO_FRAGILITY.md`.

This sensitivity is known before freezing and will be reported as
follows in all results:

1. **Primary**: Report the 5-ancestry Q (all available strata), which
   is what the pipeline computes by default. This gives non-transport.
2. **Sensitivity 1**: Report the EUR-vs-EAS Q for direct comparability
   with the other CAMeRa pair (BMI_T2D) and with the Wang 2022 pairs
   that are all EUR-vs-EAS.
3. **Sensitivity 2**: Leave-one-out (LOO) fragility analysis. Dropping
   AFR or EAS alone flips the verdict. Report as evidence that the
   non-transport classification is fragile and driven by the
   EUR/EAS-vs-AFR contrast, consistent with Mason et al.'s warning
   about underpowered strata inflating apparent heterogeneity.
4. **Discussion**: Frame this pair as a real-data demonstration that
   transportability verdicts are sensitive to which populations are
   compared --- a composite-hypothesis fragility, not a bug. This is
   a genuinely novel empirical finding, not just a limitation.

The headline Tier 1 accuracy number uses the 5-ancestry Q (primary).
A supplementary table reports accuracy under EUR-vs-EAS framing for
all multi-ancestry pairs.

### Tier 2 --- excluded from this pass (requires running MR ourselves)

27 pairs. Not run. Not included in accuracy calculations. Listed in
REPLACEMENT_PLAN.md for future work.

### Tier 3 --- domain-knowledge only, locked as non-empirical (24 pairs)

Concentrated in MS (8/9), AD (11/17), autoimmune (5/10). These get:
- Q values computed but asterisked in every table as "domain-knowledge
  strata, not independently published per-ancestry MR estimates"
- Reported in a separate accuracy number, never silently merged with
  Tier 1 as equivalent evidence

### Already exact (6 pairs)

No changes needed. Included in overall accuracy as their own category.

---

## 3. Predictions (frozen before re-running)

### H1: Spot-checked pairs hold

Smoking->SCZ (Q=1.56, p=0.21, transport) and BMI->depression (Q=36.4,
non-transport) will reproduce the same verdicts in the full pipeline
re-run. These were computed by hand from the extracted data; the pipeline
should give identical results to within floating-point precision.

### H2: Expected flips from the swap

I predict **2 pairs will flip** from their original expected labels:

1. **alcohol_CAD_MR**: Original label = non-transport. Real MVP data
   gives Q=0.71, p>0.05 -> transport. This is a genuine reclassification
   (incomparable instruments in original, consistent instruments in real
   data). Already documented in swap script reclassification_note.

2. **BMI_breast_cancer_MR**: Original label = non-transport. Assembled
   real data gives Q=2.25, p=0.13 -> transport. Both ancestries show
   protective direction (OR<1). The original non-transport label may
   have been based on the premenopausal/postmenopausal BMI-breast-cancer
   sign reversal, which is a within-ancestry subtype effect, not a
   cross-ancestry one.

The other 12 Tier 1 pairs should hold their original labels. If a third
pair flips, the most likely candidate is BMI_CAD_MR (Q=7.27 is
significant but not overwhelmingly so at alpha=0.05; a slight change in
SE handling could shift it).

Note: **LDL_stroke_MR** (original label = transport) may flip to
non-transport under the 5-ancestry Q (12.09, p=0.017). The original
label was assigned using 2 approximate strata; the 5-ancestry real
data introduces 3 additional populations (AFR, AMR, SAS) that pull
the verdict toward non-transport. If this counts as a "flip," it is
a third reclassification (alongside alcohol and breast cancer) ---
but unlike those two, it is driven by expanding the comparison set
rather than correcting the instruments. This is pre-specified as a
possible third flip; see the LOO sensitivity section above.

### H3: Accuracy range

**Tier 1 exact only (n=14, all in swap script):**
I predict 11-13 correct against original labels (79-93%). The 2
predicted flips (alcohol, breast cancer) are genuine reclassifications,
not errors --- if I exclude known reclassifications, I predict the
remaining non-reclassified pairs correct (>95%).

**Tier 1 + already-exact (n=20):** 17-19 correct (85-95%).

**All 71 pairs (Tier 1 + Tier 3 + already-exact):** The Tier 3 pairs
still use domain-knowledge strata that are likely circular. I predict
overall accuracy of 85-92%, inflated by circular Tier 3 pairs. This
number is reported for transparency but is NOT the headline.

**The headline number is Tier 1 accuracy** (the independently validated
subset). If it falls below 79% (fewer than 11 of 14 correct), this is a
genuine finding about the limitations of Q-based transportability
classification, not a failure to be smoothed over.

### H4: Zhao 2022 supplementary yield

Tables S7/S8/S16 contain per-ancestry ORs for 108 protein-disease MR
signals (7 trans-ancestry + 89 EUR-specific + 12 AFR-specific). From our
partial extraction (S16A/B/C, S11, S7B/S8B overlap), I already identified
128 total signals, 7 with transport classification, 121 non-transport.

I predict extracting the full supplementary tables will yield **at least
7 additional Tier 1 pairs** with both EUR and AFR ORs (the 7
trans-ancestry signals from S16A, most of which we have already partially
extracted). The 89 EUR-specific and 12 AFR-specific signals are by
definition single-ancestry and cannot form Tier 1 pairs on their own.

---

## 4. What counts as a deviation (log every one)

All deviations from this pre-registration will be logged in a file called
`DEVIATIONS_LOG.md` in this directory, with date, description, and
reason.

Specifically:
- Extracting numbers from Zhao 2022 S12-S15 (pQTL-level, currently
  optional) counts as a deviation if included in the pipeline.
- Any Tier 1-pending pair that gets excluded after inspection must be
  logged with the exact reason, not silently dropped.
- Any change to swap_tier1_real_data.py after this freeze gets a diff +
  reason in the deviations log.
- Both CAMeRa pairs (BMI_T2D, LDL_stroke) are now in the swap script
  as pre-specified; adding them was NOT a deviation. LDL_stroke exact
  per-ancestry estimates were extracted from the analysis repo
  (github.com/yoonsucho/camera_analysis) rendered HTML tables, not
  from figure-reading. If any numbers are later found to differ from
  section 2, log the discrepancy.
- Adding any NEW pair not listed in section 2 is a deviation.
- Changing alpha from 0.05 is a deviation.

---

## 5. Analysis plan (locked)

1. Run `swap_tier1_real_data.py` against `pairs_curated.json` to produce
   `pairs_curated_real_data.json`.
2. Run `pipeline.py` on the output file with alpha=0.05.
3. Report **three accuracy numbers**, not one:
   - (a) Accuracy on Tier 1 exact pairs only (n=14). This is the headline.
   - (b) Accuracy on the combined Tier 1 + Tier 3 + already-exact set
     (n=71), with Tier 3 clearly labeled as non-empirical in every table
     row.
   - (c) The original all-71 pre-swap number, explicitly framed as
     "superseded, shown for transparency."
4. BH-FDR correction applied across the headline set (Tier 1 exact).
5. For each pair, report: Q statistic, df, p-value, I^2, classification
   verdict, original expected label, match/mismatch, and data provenance
   tier.

---

## 6. Decision rules (locked)

- If Tier 1 accuracy falls below 79% (fewer than 11 of 14 correct):
  reported as a finding, not re-run with different assumptions.
- If a predicted flip (alcohol, breast cancer) does NOT flip: logged as
  a surprise, investigated, but the result stands.
- Any post-freeze adjustment to alpha, Q-test implementation, or
  classification rule specifically to improve the accuracy number is
  exactly the p-hacking pattern that got flagged in the original audit.
  The threshold is locked at alpha=0.05 for the Q-test chi-squared.
- Reclassified pairs (alcohol_CAD_MR) are reported both ways: (i)
  accuracy against ORIGINAL labels, (ii) accuracy against UPDATED labels
  with reclassification noted. Both numbers appear in the paper.

---

## 7. New methodological citation (not a data source)

Mason, Zuber, Hemani, Burgess et al. (2025), "Mendelian randomization in
a multi-ancestry world: reflections and practical advice"
(arXiv:2510.17554). This review by leading MR statisticians covers exactly
our question: when do cross-ancestry MR estimate differences reflect real
biology vs. artifacts. Their conclusion --- "differences in MR estimates
by ancestry group should be interpreted cautiously... corroborating
evidence of a biological mechanism... is needed" --- is independent,
authoritative support for our composite-hypothesis framing. Cite in
Discussion.

---

## 8. Potential new domain pairs (not included in this freeze)

Identified but deferred --- adding these would be a deviation:

- **TG -> endometriosis** (PLOS ONE 2024): EUR IVW OR=1.112, p=5.03e-3;
  EAS null. Real cross-ancestry MR from GLGC. Would be a new
  cardiometabolic-adjacent domain.
- **Migraine <-> psychiatric** (MVP 2025): Multi-ancestry GWAS 433K
  veterans + MR against PTSD/depression/TBI. All nulls. New domain
  candidate.

These are logged for future work, not for this pre-registration cycle.

---

## To freeze

1. Save this file.
2. `git add` this file + `swap_tier1_real_data.py` +
   `SESSION_FINDINGS_SUMMARY.md` + `REPLACEMENT_PLAN.md`.
3. Commit. The commit SHA is the timestamp.
4. Do NOT run `pipeline.py` until the commit is pushed.
