\name{vector_sheaf_q_diagonal}
\alias{vector_sheaf_q_diagonal}
\title{Multivariate sheaf Q assuming diagonal per-stratum covariance}
\usage{
vector_sheaf_q_diagonal(beta_matrix, se_matrix)
}
\arguments{
\item{beta_matrix}{Numeric matrix (K x d): per-stratum effect vectors.}
\item{se_matrix}{Numeric matrix (K x d): per-stratum standard errors.}
}
\value{
A list with components:
\describe{
  \item{Q_V}{The vector sheaf Q statistic.}
  \item{df}{Degrees of freedom: d * (K - 1).}
  \item{p}{P-value from chi-squared distribution.}
  \item{d}{Dimension of the effect vector.}
  \item{K}{Number of strata.}
  \item{sum_scalar_Q}{Sum of per-trait scalar Cochran's Q statistics.
    Equals Q_V when traits are independent.}
}
}
\description{
Simpler interface when cross-trait correlations within each stratum
are unavailable. Each stratum's covariance is diag(se^2). Returns
both the vector Q and the sum of per-trait scalar Q statistics for
comparison.
}
\examples{
beta <- matrix(c(0.30, 0.10, 0.10, 0.30, 0.20, 0.20),
               nrow = 3, byrow = TRUE)
se <- matrix(0.04, nrow = 3, ncol = 2)
result <- vector_sheaf_q_diagonal(beta, se)
result$Q_V
}
