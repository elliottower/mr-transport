\name{vector_sheaf_q_diagonal}
\alias{vector_sheaf_q_diagonal}
\title{Multivariate sheaf Q with diagonal covariance}
\usage{
vector_sheaf_q_diagonal(beta_matrix, se_matrix)
}
\arguments{
\item{beta_matrix}{Numeric matrix (K x d): per-stratum effect vectors.}
\item{se_matrix}{Numeric matrix (K x d): per-stratum standard errors.}
}
\value{
A list with components: Q_V, df, p, d, K, sum_scalar_Q.
When traits are uncorrelated (diagonal covariance), Q_V equals the
sum of d independent scalar Cochran's Q tests (sum_scalar_Q).
}
\description{
Simpler interface for \code{\link{vector_sheaf_q}} when cross-trait
correlations within each stratum are unavailable. Each stratum's
covariance matrix is diag(se^2).
}
\examples{
beta <- matrix(c(0.30, 0.10, 0.10, 0.30, 0.20, 0.20), nrow = 3, byrow = TRUE)
se <- matrix(0.04, nrow = 3, ncol = 2)
result <- vector_sheaf_q_diagonal(beta, se)
abs(result$Q_V - result$sum_scalar_Q) < 1e-10  # TRUE: diagonal => Q_V = sum
}
