# sheafq

Vector-valued sheaf Q tests for multi-trait heterogeneity in multi-ancestry meta-analyses.

## The problem

Standard Cochran's Q tests each trait independently. When effect sizes vary
across ancestries not in magnitude but in *direction* — the joint effect vector
rotates — per-trait tests often miss the heterogeneity entirely. Power
simulations show that at moderate trait correlations (rho = 0.6) and rotation
angles around 60 degrees, the vector test has ~90% power where per-trait scalar
Q has ~41%.

## The solution

`sheafq` implements the vector-valued sheaf Q statistic:

**Q_V = sum_k (beta_k - beta_bar)^T W_k (beta_k - beta_bar) ~ chi2_{d(K-1)}**

where beta_k is the d-dimensional effect vector in stratum k, W_k is the
inverse covariance, and beta_bar is the precision-weighted pooled estimate.
On a single trait (d = 1), this reduces algebraically to Cochran's Q. On
multiple traits (d > 1), it captures covariance-mediated heterogeneity that
d independent scalar tests cannot.

## Installation

```r
# From GitHub
remotes::install_github("elliottower/mr-transport", subdir = "sheafq")

# From local source
install.packages("sheafq", repos = NULL, type = "source")
```

## Quick start

```r
library(sheafq)

# Per-ancestry effect estimates at a locus for 3 blood traits
# Rows: ancestries, Columns: traits
beta <- matrix(c(
   0.30,  0.10,  0.05,
   0.10,  0.30,  0.05,
   0.20,  0.20,  0.05
), nrow = 3, byrow = TRUE)

se <- matrix(0.04, nrow = 3, ncol = 3)

# Vector sheaf Q (assuming independent traits)
result <- vector_sheaf_q_diagonal(beta, se)
result$Q_V   # 37.5
result$p     # < 0.001

# Per-trait scalar Q for comparison
for (j in 1:3) {
  sq <- scalar_cochran_q(beta[, j], se[, j])
  cat(sprintf("Trait %d: Q = %.2f, p = %.4f\n", j, sq$Q, sq$p))
}

# Classify the locus
classify_locus(beta, se)$category
# "rotation_only" — vector Q detects it, no single scalar Q does

# Where is the rotation?
rot <- max_rotation(beta)
cat(sprintf("Max rotation: %.1f degrees\n", rot$theta_max))
```

## With trait correlations

When traits are measured in the same sample, their estimation errors are
correlated. If you have the phenotypic correlation matrix:

```r
rho <- matrix(c(1, 0.6, 0.3,
                0.6, 1, 0.4,
                0.3, 0.4, 1), nrow = 3)

result_corr <- vector_sheaf_q_correlated(beta, se, rho)
result_corr$Q_V / result_corr$sum_scalar_Q  # > 1 when rotation is present
```

The ratio Q_V / sum(scalar Q) exceeding 1.0 is the signature of rotation:
covariance structure amplifies the joint signal beyond what per-trait tests see.

## Functions

| Function | Description |
|---|---|
| `scalar_cochran_q()` | Standard Cochran's Q heterogeneity test (d = 1) |
| `vector_sheaf_q()` | Multivariate sheaf Q with full covariance matrices |
| `vector_sheaf_q_diagonal()` | Sheaf Q assuming independent traits |
| `vector_sheaf_q_correlated()` | Sheaf Q with within-stratum trait correlations |
| `rotation_angle()` | Angle between two effect vectors (degrees) |
| `max_rotation()` | Maximum pairwise rotation across strata |
| `classify_locus()` | Classify locus as concordant / rotation-only / component-only |

## Tutorial

See the package vignette for a full walkthrough:

```r
vignette("tutorial", package = "sheafq")
```

## Mathematical properties

Three invariants that `sheafq` satisfies (and tests verify):

1. **Scalar equivalence**: At d = 1, `vector_sheaf_q` returns identical Q and p
   to `scalar_cochran_q`.
2. **Diagonal decomposition**: With diagonal covariance (independent traits),
   Q_V equals the sum of per-trait scalar Q tests.
3. **Correlated divergence**: With off-diagonal covariance and rotation-like
   heterogeneity, Q_V exceeds the sum of scalar Q tests.

## Citation

Tower, E. (2026). Vector-valued sheaf Q tests for heterogeneity in
multi-ancestry Mendelian randomization. *Manuscript in preparation.*
