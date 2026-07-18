\name{vector_sheaf_q_correlated}
\alias{vector_sheaf_q_correlated}
\title{Multivariate sheaf Q with within-stratum trait correlations}
\usage{
vector_sheaf_q_correlated(beta_matrix, se_matrix, rho_matrix)
}
\arguments{
\item{beta_matrix}{Numeric matrix (K x d): per-stratum effect vectors.}
\item{se_matrix}{Numeric matrix (K x d): per-stratum standard errors.}
\item{rho_matrix}{Numeric matrix (d x d): phenotypic correlation matrix
  across traits.}
}
\value{
A list with components:
\describe{
  \item{Q_V}{The vector sheaf Q statistic.}
  \item{df}{Degrees of freedom: d * (K - 1).}
  \item{p}{P-value from chi-squared distribution.}
  \item{d}{Dimension of the effect vector.}
  \item{K}{Number of strata.}
  \item{sum_scalar_Q}{Sum of per-trait scalar Cochran's Q statistics.}
}
}
\description{
In biobank data (same individuals, multiple traits), the within-stratum
covariance of effect estimates at a locus is:
\code{Sigma_k[j,l] = rho_jl * SE_kj * SE_kl}.
This function builds the full covariance matrices from the standard
errors and a phenotypic correlation matrix.
}
\examples{
beta <- matrix(c(0.30, 0.10, 0.10, 0.30, 0.20, 0.20),
               nrow = 3, byrow = TRUE)
se <- matrix(0.04, nrow = 3, ncol = 2)
rho <- matrix(c(1, 0.6, 0.6, 1), nrow = 2)
result <- vector_sheaf_q_correlated(beta, se, rho)
result$Q_V
}
