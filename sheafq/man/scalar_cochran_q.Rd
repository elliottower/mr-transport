\name{scalar_cochran_q}
\alias{scalar_cochran_q}
\title{Standard Cochran's Q for scalar effect estimates}
\usage{
scalar_cochran_q(betas, ses)
}
\arguments{
\item{betas}{Numeric vector of length K: per-stratum effect estimates.}
\item{ses}{Numeric vector of length K: per-stratum standard errors.}
}
\value{
A list with components:
\describe{
  \item{Q}{The Cochran's Q statistic.}
  \item{df}{Degrees of freedom (K - 1).}
  \item{p}{P-value from chi-squared distribution.}
  \item{I2}{I-squared heterogeneity measure.}
  \item{tau2}{DerSimonian-Laird between-study variance estimate.}
  \item{beta_pooled}{Inverse-variance weighted pooled estimate.}
}
}
\description{
Computes Cochran's Q heterogeneity statistic for a set of scalar effect
estimates with known standard errors. Under the null hypothesis of no
between-stratum heterogeneity, Q follows a chi-squared distribution
with K - 1 degrees of freedom.
}
\examples{
betas <- c(0.30, 0.25, 0.15)
ses <- c(0.05, 0.06, 0.08)
result <- scalar_cochran_q(betas, ses)
result$Q   # 2.5396
result$p   # 0.2809
}
