\name{vector_sheaf_q}
\alias{vector_sheaf_q}
\title{Multivariate sheaf Q for vector-valued stalks}
\usage{
vector_sheaf_q(beta_matrix, cov_matrices)
}
\arguments{
\item{beta_matrix}{Numeric matrix (K x d): per-stratum effect vectors.}
\item{cov_matrices}{3D array (K x d x d): per-stratum covariance matrices.}
}
\value{
A list with components:
\describe{
  \item{Q_V}{The vector sheaf Q statistic.}
  \item{df}{Degrees of freedom: d * (K - 1).}
  \item{p}{P-value from chi-squared distribution.}
  \item{d}{Dimension of the effect vector.}
  \item{K}{Number of strata.}
}
}
\description{
Computes the multivariate Cochran's Q statistic on vector-valued
effect estimates. Each stratum contributes a d-dimensional effect
vector with a d x d covariance matrix. Under the null of no
between-stratum heterogeneity, Q_V follows a chi-squared distribution
with d * (K - 1) degrees of freedom.
}
\examples{
beta <- matrix(c(0.30, 0.10, 0.10, 0.30, 0.20, 0.20),
               nrow = 3, byrow = TRUE)
K <- 3; d <- 2
cov_arr <- array(0, dim = c(K, d, d))
for (k in 1:K) cov_arr[k, , ] <- diag(rep(0.04^2, d))
result <- vector_sheaf_q(beta, cov_arr)
result$Q_V
}
