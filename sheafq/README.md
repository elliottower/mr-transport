# sheafq

Vector-valued sheaf Q tests for multi-trait heterogeneity in multi-ancestry meta-analyses.

## Installation

```r
# Install from local source
install.packages("sheafq", repos = NULL, type = "source")

# Or with devtools/remotes from GitHub (once published)
# remotes::install_github("elliottower/sheafq")
```

## Quick start

```r
library(sheafq)

# --- Scalar: Cochran's Q ---
betas <- c(0.30, 0.25, 0.15)
ses   <- c(0.05, 0.06, 0.08)
scalar_cochran_q(betas, ses)
# $Q = 2.54, $p = 0.28

# --- Vector Q with diagonal covariance ---
# 3 ancestries, 2 traits: effect vector rotates
beta <- matrix(c(0.30, 0.10,
                 0.10, 0.30,
                 0.20, 0.20), nrow = 3, byrow = TRUE)
se <- matrix(0.04, nrow = 3, ncol = 2)

result <- vector_sheaf_q_diagonal(beta, se)
result$Q_V           # 25.0
result$sum_scalar_Q  # 25.0 (diagonal => Q_V = sum)

# --- Vector Q with trait correlations ---
rho <- matrix(c(1, 0.6, 0.6, 1), nrow = 2)
result_corr <- vector_sheaf_q_correlated(beta, se, rho)
result_corr$Q_V                        # 62.5 (diverges upward)
result_corr$Q_V / result_corr$sum_scalar_Q  # 2.5

# --- Locus classification ---
classify_locus(beta, se)$category  # "rotation_only" or "concordant_significant"

# --- Rotation angles ---
rotation_angle(c(0.30, 0.10), c(0.10, 0.30))  # 53.1 degrees
max_rotation(beta)$theta_max                     # 53.1 degrees
```

## Key idea

On scalar stalks (d = 1), sheaf Q reduces algebraically to Cochran's Q.
On vector-valued stalks (d > 1), the multivariate sheaf Q detects
**effect vector rotation** — where per-trait effect magnitudes are preserved
but the joint direction of the effect vector changes across populations —
that d independent scalar Q tests cannot detect.

## Functions

| Function | Description |
|---|---|
| `scalar_cochran_q` | Standard Cochran's Q heterogeneity test |
| `vector_sheaf_q` | Multivariate sheaf Q with full covariance matrices |
| `vector_sheaf_q_diagonal` | Sheaf Q assuming independent traits (diagonal covariance) |
| `vector_sheaf_q_correlated` | Sheaf Q with within-stratum trait correlations |
| `rotation_angle` | Angle between two effect vectors (degrees) |
| `max_rotation` | Maximum pairwise rotation across strata |
| `classify_locus` | Classify locus as concordant / rotation-only / component-only |
