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
across traits (shared across strata).}
}
\value{
A list with components: Q_V, df, p, d, K, sum_scalar_Q.
When traits are correlated (rho != I), Q_V differs from sum_scalar_Q.
}
\description{
In biobank data where the same individuals contribute to multiple trait
GWAS, within-stratum effect estimates are correlated. The covariance is
Sigma_k[j,l] = rho_jl * SE_kj * SE_kl, where rho_jl is the phenotypic
correlation between traits j and l.

With correlated traits, the vector Q_V captures coordinated rotation of
the effect vector across strata that d independent scalar Q tests miss.
}
\examples{
beta <- matrix(c(0.30, 0.10, 0.10, 0.30, 0.20, 0.20), nrow = 3, byrow = TRUE)
se <- matrix(0.04, nrow = 3, ncol = 2)
rho <- matrix(c(1, 0.6, 0.6, 1), nrow = 2)
result <- vector_sheaf_q_correlated(beta, se, rho)
result$Q_V / result$sum_scalar_Q  # > 1: correlated Q_V diverges from sum
}
