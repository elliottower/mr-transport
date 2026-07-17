# LDL_stroke_MR: Leave-One-Out Fragility Analysis

Source: Hemani 2025 CAMeRa analysis repo (github.com/yoonsucho/camera_analysis)
Data: mr.html kable table, FEMA instrument selection (strategy C)
Computed: before SHA freeze, pre-registered as sensitivity analysis

## Per-ancestry estimates (LDL cholesterol -> any stroke)

| Ancestry | logOR | SE | p-value | Qj | Qj p |
|----------|-------|-------|---------|------|------|
| EUR | 0.0811 | 0.0185 | 1.3e-5 | 0.24 | 0.625 |
| EAS | 0.0221 | 0.0272 | 0.417 | 3.36 | 0.067 |
| AFR | 0.2852 | 0.0826 | 5.7e-4 | 6.66 | 0.010 |
| AMR | 0.3016 | 0.2049 | 0.141 | 1.26 | 0.262 |
| SAS | 0.2061 | 0.1778 | 0.247 | 0.57 | 0.451 |

## 5-ancestry overall

Q = 12.09, df = 4, p = 0.017 -> **NON-TRANSPORT**

## Leave-one-out analysis

| Dropped | Q | df | p | Verdict | Flips? |
|---------|---|----|-------|---------|--------|
| None | 12.09 | 4 | 0.017 | non-transport | — |
| EUR | 11.40 | 3 | 0.010 | non-transport | no |
| EAS | 7.27 | 3 | 0.063 | transport | YES |
| AFR | 5.20 | 3 | 0.156 | transport | YES |
| AMR | 10.83 | 3 | 0.013 | non-transport | no |
| SAS | 11.52 | 3 | 0.009 | non-transport | no |

**Interpretation**: The non-transport verdict is fragile. Dropping
EITHER EAS or AFR alone flips the classification. The heterogeneity
is driven by the contrast between:
- EUR/EAS (small protective effects, ~0.02-0.08)
- AFR/AMR/SAS (larger effects, ~0.21-0.30)

AFR contributes most to Q (Qj=6.66 of total 12.09, i.e. 55%). But
EAS also matters: it pulls the pooled estimate downward, creating
tension with AFR/AMR/SAS. Dropping EAS raises the pooled estimate
enough that AFR no longer looks anomalous.

## Pairwise Q tests

Only EUR-vs-AFR and EAS-vs-AFR show significant heterogeneity:

| Pair | Q | p | Verdict |
|------|---|-------|---------|
| EUR vs EAS | 3.21 | 0.070 | transport |
| EUR vs AFR | 5.82 | 0.015 | non-transport |
| EUR vs AMR | 1.15 | 0.284 | transport |
| EUR vs SAS | 0.49 | 0.492 | transport |
| EAS vs AFR | 9.15 | 0.003 | non-transport |
| EAS vs AMR | 1.83 | 0.172 | transport |
| EAS vs SAS | 1.05 | 0.307 | transport |
| AFR vs AMR | 0.01 | 1.000 | transport |
| AFR vs SAS | 0.16 | 1.000 | transport |
| AMR vs SAS | 0.12 | 1.000 | transport |

## Key takeaway for the paper

This pair is a real-data demonstration that "transportable" vs.
"non-transportable" is not a fixed property of an exposure-outcome
relationship — it depends on which populations are compared. The AFR
estimate for LDL->stroke (logOR=0.285, SE=0.083) is ~3.5x larger
than the EUR estimate (0.081), with a relatively tight CI that
excludes the EUR point estimate. This is either:
(a) a genuine ancestry-specific effect size (Mason pathway 5), or
(b) an artifact of different LD, allele frequencies, or confounding
    structure in AFR samples (Mason pathways 1-4).

The fact that AFR sample sizes for stroke GWAS are much smaller than
EUR, combined with the known enrichment of population-specific LD
patterns in AFR populations, makes (b) plausible. CAMeRa's FEMA
instrument selection mitigates some of this, but cannot fully resolve it.

This result strengthens the composite-hypothesis framing: a single
Q-test cannot distinguish real biology from methodological artifact.
