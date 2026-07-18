\name{test_transport}
\alias{test_transport}
\title{Test whether stratified MR estimates are transportable}
\usage{
test_transport(betas, ses, strata_names = NULL, alpha = 0.05)
}
\arguments{
\item{betas}{Numeric vector of per-stratum causal effect estimates
  (log-OR or beta scale).}
\item{ses}{Numeric vector of per-stratum standard errors, same length
  as \code{betas}.}
\item{strata_names}{Optional character vector of stratum labels (e.g.
  ancestry names). If NULL, strata are unnamed.}
\item{alpha}{Significance threshold for the Q test.}
}
\value{
A list with components:
\describe{
  \item{Q}{Cochran's Q statistic.}
  \item{df}{Degrees of freedom (k - 1).}
  \item{p}{P-value from the chi-squared distribution.}
  \item{I2}{I-squared heterogeneity measure (0 to 1).}
  \item{tau2}{DerSimonian-Laird between-stratum variance estimate.}
  \item{power}{Post-hoc power of the Q test.}
  \item{verdict}{Either "transport" or "non-transport".}
  \item{beta_pooled}{Inverse-variance weighted pooled estimate.}
  \item{k}{Number of strata.}
  \item{strata_names}{Character vector of stratum labels or NULL.}
  \item{is_transportable}{Logical: TRUE if verdict is "transport".}
  \item{underpowered}{Logical: TRUE if verdict is "transport" but
    power < 0.50 and I2 > 0.30.}
}
}
\description{
Runs Cochran's Q heterogeneity test on a set of per-stratum causal effect
estimates, computes post-hoc power using the noncentral chi-squared
distribution, and returns a verdict of "transport" (Q not significant) or
"non-transport" (Q significant at level alpha).
}
\examples{
result <- test_transport(
  betas = c(1.6, 1.2, 0.8, 1.0),
  ses = c(0.04, 0.07, 0.12, 0.10),
  strata_names = c("EUR", "EAS", "AFR", "HISP")
)
result$verdict   # "non-transport"
result$power     # high
}
