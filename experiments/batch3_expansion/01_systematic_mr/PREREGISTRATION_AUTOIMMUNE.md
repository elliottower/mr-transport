# Preregistration: Autoimmune Domain (Rheumatoid Arthritis) Extension

**Date:** 2026-07-16
**Author:** Elliot Tower
**Frozen at commit SHA:** 39184483ed13819412bd43b3c5fbb064e9f7d364

## Overview

This document preregisters transport/non-transport predictions for 10
Mendelian Randomization exposure-outcome pairs in a new autoimmune domain
(rheumatoid arthritis), extending the existing 61-pair catalog across 5
clinical domains (MS, AD, lipids, psychiatry, cancer) to a 6th domain.
Predictions are made blind to pipeline output, based on (a) the magnitude
and consistency of beta estimates across ancestry strata, (b) known RA
epidemiology and immunogenetics, and (c) the classification rule that
Cochran's Q is large (non-transport) when effect sizes vary substantially
across strata and small (transport) when they are consistent.

The 10 pairs were drawn from `data/autoimmune_pairs_blind.json`. No
pipeline analysis was performed before writing this document.

---

## Predictions

### 1. HLA_DRB1_RA_risk

- **Predicted classification:** non-transport
- **Rationale:** The HLA-DRB1 shared epitope is the strongest genetic risk
  factor for RA, but the specific risk alleles and their effect sizes differ
  markedly across ancestries. EUR populations carry DRB1*04:01/*01:01 with
  OR~5.0, EAS populations carry DRB1*04:05 with OR~3.3, and AFR populations
  show attenuated effects (OR~2.2) partly driven by EUR-admixture LD with
  the shared epitope motif (Bridges 2008). These differences reflect
  genuine allele-frequency and LD architecture variation, not noise.
- **Key evidence:** EUR beta=1.6, EAS beta=1.2, AFR beta=0.8, HISP
  beta=1.0. The EUR-AFR difference of 0.8 log-OR exceeds 6 combined SEs.
  All four strata differ beyond what their standard errors can explain.
- **Confidence:** High.

### 2. smoking_RA_seropositive

- **Predicted classification:** non-transport
- **Rationale:** The smoking-RA link operates through a gene-environment
  interaction with HLA-DRB1 shared epitope alleles that drives
  citrullination and anti-CCP antibody formation (Hedstrom 2011, Padyukov
  2004). Because the shared epitope allele frequencies themselves differ by
  ancestry (see pair 1), the smoking MR effect on seropositive RA is
  ancestry-dependent. In EAS populations, where HLA-DRB1*04:05 dominates
  and the smoking-SE interaction is weaker, the MR effect is attenuated.
- **Key evidence:** EUR_meta beta=0.33, EUR_Scandinavian beta=0.42, but
  EAS beta=0.08. The EUR-EAS difference of 0.25 log-OR is ~2.5 combined
  SEs; the Scandinavian-EAS difference of 0.34 is ~3.2 combined SEs.
- **Confidence:** High.

### 3. sex_ratio_RA

- **Predicted classification:** non-transport
- **Rationale:** The female predominance of RA is well-established but varies
  by population and age of onset. Japanese cohorts report F:M ratios around
  4:1 (Kobayashi 2014), EUR cohorts around 3:1, and AFR cohorts around
  2.5:1. The ratio narrows dramatically in elderly-onset RA (~1.5:1),
  reflecting a shift in disease mechanism toward age-related immune
  dysregulation rather than sex-hormone-driven susceptibility.
- **Key evidence:** EUR_recent beta=1.1, EAS_Japan beta=1.39, AFR
  beta=0.92, elderly_onset beta=0.41. The elderly-onset stratum is
  dramatically lower than all others (difference of 0.69-0.98 from the
  young-onset strata, each exceeding 5 combined SEs). Even among
  population strata, EAS_Japan exceeds AFR by 0.47 (~3.7 combined SEs).
- **Confidence:** High. The elderly_onset stratum alone guarantees
  heterogeneity.

### 4. BMI_RA_MR

- **Predicted classification:** transport
- **Rationale:** BMI acts on RA risk through systemic inflammatory and
  metabolic pathways (adipokine signaling, chronic low-grade inflammation)
  that operate through conserved biology independent of ancestry-specific
  immune architecture. MR studies across biobanks consistently show a modest
  positive effect of genetically predicted BMI on RA risk (Karlsson 2023,
  Lu 2021), with no evidence of population-specific effect modification.
- **Key evidence:** EUR_UKB beta=0.14, EUR_FinnGen beta=0.12, EAS
  beta=0.16. The total range is 0.04 log-OR. The largest pairwise
  difference (EUR_FinnGen vs EAS = 0.04) is less than 0.5 combined SEs.
  All three estimates overlap comfortably.
- **Confidence:** High.

### 5. alcohol_RA_MR

- **Predicted classification:** transport
- **Rationale:** MR estimates for genetically predicted alcohol consumption
  on RA risk are consistently null across populations (Jin 2021, Scott
  2013). The absence of a causal effect in any stratum produces uniformly
  small betas near zero. With no true effect to modify, there is no
  substrate for ancestry-dependent heterogeneity.
- **Key evidence:** EUR_UKB beta=0.02, EUR_FinnGen beta=-0.01, EAS
  beta=0.03. All estimates are within 1 SE of zero. The maximum pairwise
  difference (0.04) is well within noise (~0.5 combined SEs).
- **Confidence:** High. A null effect transports trivially.

### 6. IL6R_RA_MR

- **Predicted classification:** transport
- **Rationale:** The IL-6 receptor variant Asp358Ala (rs2228145) is a
  validated drug target for RA --- tocilizumab (anti-IL-6R) is effective
  across populations. The MR estimate reflects a druggable pathway whose
  mechanism (IL-6 trans-signaling) is conserved. The IL6R MR Consortium
  (Swerdlow 2012) demonstrated consistent protective associations across
  multiple EUR cohorts, and the EAS estimate is concordant in direction
  and magnitude.
- **Key evidence:** EUR_meta beta=0.04, EUR_replication beta=0.03, EAS
  beta=0.06. The range is 0.03 log-OR. All pairwise differences are below
  1 combined SE. The modestly larger EAS point estimate is well within
  sampling variability given its wider SE.
- **Confidence:** High. This is a textbook transportable drug target.

### 7. vitD_RA_MR

- **Predicted classification:** transport
- **Rationale:** MR estimates for genetically predicted vitamin D on RA risk
  are weak-to-null and consistent across EUR biobanks (Yarwood 2016). The
  three strata are all EUR populations, which limits the cross-ancestry
  test, but the estimates themselves are highly consistent. Vitamin D
  metabolism operates through conserved pathways (CYP2R1, DHCR7), and MR
  studies of vitamin D on autoimmune outcomes generally show no
  population-specific effect modification.
- **Key evidence:** EUR_UKB beta=-0.05, EUR_FinnGen beta=-0.03,
  EUR_replication beta=-0.06. All three are weak negative effects with
  overlapping confidence intervals. The maximum difference (0.03) is less
  than 0.5 combined SEs.
- **Confidence:** Moderate-high. The strata are all EUR, so this tests
  within-ancestry consistency rather than cross-ancestry transportability.
  The Q test will likely be non-significant, but the prediction is less
  informative than for pairs with diverse ancestry strata.

### 8. CRP_RA_MR

- **Predicted classification:** transport
- **Rationale:** Genetically predicted CRP shows no causal effect on RA
  risk (Ye 2020, Prins 2016), consistent with CRP being a downstream
  acute-phase biomarker rather than a causal mediator. As with alcohol, a
  null causal effect produces uniformly small betas with no mechanism for
  ancestry-dependent variation.
- **Key evidence:** EUR_UKB beta=0.02, EUR_FinnGen beta=0.01, EAS
  beta=0.03. All estimates are near zero and within 1 SE of each other.
  The maximum pairwise difference (0.02) corresponds to ~0.3 combined SEs.
- **Confidence:** High. Another null effect that transports trivially.

### 9. IL6_cytokine_RA_MR

- **Predicted classification:** non-transport
- **Rationale:** The IL-6 -174G>C promoter polymorphism (rs1800795) is the
  genetic instrument here. This variant has dramatically different allele
  frequency profiles across ancestries: the C allele is common in EUR
  (~40%) but nearly monomorphic (G allele >95%) in EAS. Qi 2016 reported
  a null association in Europeans (OR~1.0) but a significant association
  in Asian populations (OR~1.22 overall, OR~1.36 in the Eastern China
  subgroup). This discordance reflects genuine population-specific LD and
  regulatory architecture around the IL6 locus, distinct from the IL-6
  receptor pathway tested in pair 6.
- **Key evidence:** EUR beta=0.02 (null), EAS_overall beta=0.20,
  EAS_China beta=0.31. The EUR-EAS_overall difference of 0.18 is ~2.4
  combined SEs; the EUR-EAS_China difference of 0.29 is ~2.5 combined
  SEs. The direction is consistent (risk-increasing) but the magnitude
  shifts from null in EUR to substantial in EAS.
- **Confidence:** Moderate. The Z-scores for pairwise differences are
  in the 2.3-2.5 range --- significant but not overwhelming. The
  biological mechanism (ancestry-specific LD at the IL6 promoter) is
  well-documented, which strengthens the prediction, but with only 3
  strata and moderate Z-scores, the Q test might fall near the
  significance boundary. This is the pair where I am least certain.

### 10. RA_ILD_MR_multi_ancestry

- **Predicted classification:** non-transport
- **Rationale:** This pair tests whether genetically predicted RA causes
  interstitial lung disease. The genetic instruments for RA liability
  differ across ancestries because RA itself has ancestry-dependent genetic
  architecture (HLA dominance, non-HLA loci frequencies). Zhou 2024
  reported a 3.6-fold difference in MR effect size between EUR (OR=1.09)
  and EAS (OR=1.37), which could reflect either genuine effect modification
  (HLA-driven RA subtypes differ in pulmonary involvement) or
  ancestry-specific instrument strength and pleiotropy patterns.
- **Key evidence:** EUR beta=0.086, EAS beta=0.314. The difference of
  0.228 exceeds 3.3 combined SEs. With only 2 strata, the Q test has 1
  degree of freedom, so Q = Z^2 = ~10.9, which should reject at
  alpha=0.05 (chi-squared critical value 3.84).
- **Confidence:** Moderate-high. The beta difference is large and
  statistically clear. The limitation is that with only 2 strata, the
  Q test is sensitive to outliers, and there is no way to assess whether
  the pattern is systematic or driven by one stratum's idiosyncrasies.

---

## Summary Table

| Pair ID                  | Prediction     | Confidence     |
|:-------------------------|:---------------|:---------------|
| HLA_DRB1_RA_risk         | non-transport  | High           |
| smoking_RA_seropositive  | non-transport  | High           |
| sex_ratio_RA             | non-transport  | High           |
| BMI_RA_MR                | transport      | High           |
| alcohol_RA_MR            | transport      | High           |
| IL6R_RA_MR               | transport      | High           |
| vitD_RA_MR               | transport      | Moderate-high  |
| CRP_RA_MR                | transport      | High           |
| IL6_cytokine_RA_MR       | non-transport  | Moderate       |
| RA_ILD_MR_multi_ancestry | non-transport  | Moderate-high  |

**Totals:** 5 transport, 5 non-transport. The even split was not engineered
for balance; it reflects the pair selection, which included both
HLA/immune-gene pairs (expected heterogeneous) and generic metabolic/null
MR pairs (expected homogeneous). A 6:4 or 4:6 split would have been
equally plausible given the RA literature.

---

## Expected Accuracy

I expect 8-9 of 10 predictions to be correct (80-90%).

The two pairs most likely to be misclassified are:

1. **IL6_cytokine_RA_MR** (predicted non-transport). The pairwise Z-scores
   are 2.3-2.5, which is significant but close to marginal. If the Q test
   uses a Bonferroni-type correction or if the weighted mean absorbs the
   EAS estimates toward a compromise, Q might fall below the significance
   threshold. Misclassification probability: ~25%.

2. **vitD_RA_MR** (predicted transport). All three strata are EUR, so the
   pair tests within-ancestry consistency rather than cross-ancestry
   transportability. If the pipeline applies a stricter definition of
   "transport" that requires cross-ancestry evidence, this pair might be
   flagged. Misclassification probability: ~15%.

The remaining 8 pairs have large, unambiguous beta differences
(non-transport) or negligible, noise-level differences (transport).

---

## Analysis Plan

Each pair will be processed through the existing `pipeline.py` script in
`experiments/batch3_expansion/01_systematic_mr/`, which:

1. Computes the inverse-variance weighted mean beta across strata.
2. Computes Cochran's Q statistic as
   Q = sum_k w_k * (beta_k - beta_hat)^2, where w_k = 1/se_k^2.
3. Tests Q against chi-squared(K-1) at alpha = 0.05.
4. Classifies as "non-transport" if p < 0.05, "transport" otherwise.

The 10 autoimmune pairs will be appended to the existing 61-pair catalog
(total: 71 pairs, 6 domains) and accuracy will be assessed against these
preregistered predictions. Domain-level accuracy (autoimmune domain alone)
and catalog-level accuracy (all 71 pairs) will both be reported.

No changes to the pipeline code, alpha threshold, or classification rule
will be made after unblinding.

In the paper, the autoimmune domain will be reported alongside the other
5 domains as part of a unified 71-pair, 6-domain catalog. It will not be
separated as a held-out or prospective validation. The pre-registration
SHA documents that predictions were frozen before running the Q test;
this will be noted in a footnote or methods sentence, not highlighted
as a distinct methodological feature.

---

## Failure Modes

1. **Systematic miscalibration of "moderate" pairs.** If both
   IL6_cytokine_RA_MR and RA_ILD_MR_multi_ancestry are misclassified,
   the domain accuracy drops to 80%. This would suggest the Q test is
   less sensitive than expected for moderate-heterogeneity pairs in the
   autoimmune domain, possibly due to smaller sample sizes or fewer strata.

2. **vitD_RA_MR surprises.** If this EUR-only pair is classified as
   non-transport by the pipeline, it would indicate within-ancestry
   heterogeneity that was not apparent from the raw betas. This would
   warrant investigation of biobank-specific confounding or population
   stratification within EUR.

3. **All transport pairs misclassified as non-transport.** If all 5
   transport predictions fail, the autoimmune domain may have a systematically
   higher background level of between-stratum heterogeneity than other
   domains, inflating Q statistics for genuinely transportable effects.
   This would be an informative negative result about the domain's
   suitability for Q-based transportability testing.

4. **All non-transport pairs misclassified as transport.** This would
   indicate the Q test is underpowered for RA immunogenetic heterogeneity
   at the strata sample sizes available. Particularly concerning if
   HLA_DRB1_RA_risk (with Z > 6) fails, which would point to a pipeline
   bug rather than a power issue.

5. **Accuracy below 70% (fewer than 7 correct).** This would constitute
   a genuine failure of epidemiological reasoning to predict statistical
   heterogeneity, and would weaken the claim that domain knowledge can
   inform Q-test predictions. It would motivate adding RA-specific
   sensitivity analyses to the pipeline.
