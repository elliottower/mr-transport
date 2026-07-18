# mrtransport

Transportability testing for Mendelian randomization. Tests whether
stratified MR causal effect estimates are transportable across
populations using Cochran's Q with post-hoc power analysis, sensitivity
diagnostics, and simulation utilities. For multi-trait loci, implements
the multivariate sheaf Q statistic that detects effect vector rotation
invisible to per-trait scalar Q tests.

## Installation

```r
# Install from GitHub
remotes::install_github("elliottower/mr-transport", subdir = "mrtransport")
```

## Scalar transportability testing

The main entry point is `test_transport()`, which runs Cochran's Q on
per-stratum causal effect estimates, computes post-hoc power, and
returns a "transport" or "non-transport" verdict.

```r
library(mrtransport)

# HLA-DRB1 shared epitope -> RA: dramatic cross-ancestry variation
result <- test_transport(
  betas = c(1.6, 1.2, 0.8, 1.0),
  ses   = c(0.04, 0.07, 0.12, 0.10),
  strata_names = c("EUR", "EAS", "AFR", "HISP")
)
result$verdict        # "non-transport"
result$I2             # high
result$power          # high (plenty of signal)
```

When the test reports "transport" (non-significant Q), check whether it
had enough power to detect heterogeneity. The `underpowered` flag
triggers when the verdict is "transport" but power < 0.50 and I2 > 0.30:

```r
result <- test_transport(
  betas = c(0.10, -0.05, 0.15, 0.02),
  ses   = c(0.04, 0.05, 0.08, 0.10),
  strata_names = c("EUR_midlife", "EUR_latelife", "EAS", "AFR")
)
result$underpowered   # TRUE: honest uncertainty, not evidence of homogeneity

# How many strata would you need?
strata_needed(I2 = result$I2, target_power = 0.80)
```

### Sensitivity analysis

```r
# Does the verdict depend on a single stratum?
loo <- leave_one_out(
  betas = c(0.25, 0.23, 0.28),
  ses   = c(0.05, 0.06, 0.07),
  strata_names = c("EUR", "EAS", "AFR")
)
loo$stable

# How does the verdict change across significance thresholds?
sweep <- alpha_sweep(
  betas = c(0.25, 0.23, 0.28),
  ses   = c(0.05, 0.06, 0.07)
)
sweep
```

### Simulation

```r
# Generate synthetic pairs with known ground truth
pair <- simulate_pair(k = 4, seed = 42)
catalog <- simulate_catalog(n_transport = 20, n_nontransport = 10, seed = 42)
```

## Vector sheaf Q (multi-trait loci)

When a locus affects multiple traits, per-trait Cochran's Q can miss
coordinated heterogeneity -- effect vector rotation across populations.
The vector sheaf Q statistic detects this.

```r
# Per-ancestry effect estimates at a multi-trait locus (K=6, d=5)
beta <- matrix(c(
   0.15,  0.08,  0.03,  0.12,  0.02,
   0.18,  0.10,  0.02,  0.14,  0.03,
  -0.25,  0.35,  0.20, -0.10,  0.15,
   0.12,  0.06,  0.04,  0.10,  0.01,
   0.08,  0.12,  0.06,  0.05,  0.04,
   0.14,  0.09,  0.03,  0.11,  0.02
), nrow = 6, byrow = TRUE)

se <- matrix(c(
  0.02, 0.02, 0.01, 0.02, 0.01,
  0.03, 0.03, 0.02, 0.03, 0.02,
  0.04, 0.04, 0.03, 0.04, 0.03,
  0.03, 0.03, 0.02, 0.03, 0.02,
  0.04, 0.04, 0.03, 0.04, 0.03,
  0.03, 0.03, 0.02, 0.03, 0.02
), nrow = 6, byrow = TRUE)

# Vector Q with diagonal covariance
result <- vector_sheaf_q_diagonal(beta, se)
result$Q_V
result$p

# With known trait correlations
rho <- matrix(0.4, nrow = 5, ncol = 5)
diag(rho) <- 1
result_corr <- vector_sheaf_q_correlated(beta, se, rho)

# Classify: concordant, rotation-only, or component-only
cl <- classify_locus(beta, se)
cl$category

# Maximum rotation angle
rot <- max_rotation(beta)
rot$theta_max
```

## Functions

### Scalar transportability
- `test_transport()` -- Main test: Q + power + verdict
- `transport_power()` -- Post-hoc power via noncentral chi-squared
- `strata_needed()` -- Sample size planning for strata
- `scalar_cochran_q()` -- Raw Cochran's Q computation

### Sensitivity
- `leave_one_out()` -- Verdict stability under stratum removal
- `alpha_sweep()` -- Verdict across significance thresholds

### Vector sheaf Q
- `vector_sheaf_q()` -- Full multivariate Q with arbitrary covariance
- `vector_sheaf_q_diagonal()` -- Diagonal covariance (independent traits)
- `vector_sheaf_q_correlated()` -- Correlated traits via phenotypic rho

### Classification and geometry
- `classify_locus()` -- Four-way classification of multi-trait loci
- `rotation_angle()` -- Angle between two effect vectors
- `max_rotation()` -- Maximum pairwise rotation across strata

### Simulation
- `simulate_pair()` -- One synthetic pair with known ground truth
- `simulate_catalog()` -- Batch of synthetic pairs for benchmarking

## License

MIT
