\name{vector_sheaf_q}
\alias{vector_sheaf_q}
\title{Multivariate sheaf Q for vector-valued stalks}
\usage{
vector_sheaf_q(beta_matrix, cov_matrices)
}
\arguments{
\item{beta_matrix}{Numeric matrix (K x d): per-stratum effect vectors.
K strata, d traits.}
\item{cov_matrices}{3D array (K x d x d): per-stratum covariance matrices.}
}
\value{
A list with components:
\describe{
  \item{Q_V}{The vector-valued sheaf Q statistic.}
  \item{df}{Degrees of freedom: d * (K - 1).}
  \item{p}{P-value from chi-squared distribution.}
  \item{d}{Number of traits.}
  \item{K}{Number of strata.}
}
}
\description{
Computes the multivariate sheaf Q statistic for detecting heterogeneity
in vector-valued effect estimates across K strata. When d = 1, this
reduces algebraically to Cochran's Q. When d > 1, cross-component
covariance detects effect vector rotation invisible to per-trait scalar
tests.

Under the null hypothesis of no between-stratum heterogeneity,
Q_V follows a chi-squared distribution with d * (K - 1) degrees of
freedom.
}
\examples{
# d=1 case: should match scalar Cochran's Q
betas_1d <- matrix(c(0.30, 0.25, 0.15), ncol = 1)
covs_1d <- array(c(0.05, 0.06, 0.08)^2, dim = c(3, 1, 1))
vector_sheaf_q(betas_1d, covs_1d)$Q_V  # 2.5396
}
