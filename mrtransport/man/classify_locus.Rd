\name{classify_locus}
\alias{classify_locus}
\title{Classify a locus as concordant, rotation-only, or component-only}
\usage{
classify_locus(beta_matrix, se_matrix, alpha = 0.05)
}
\arguments{
\item{beta_matrix}{Numeric matrix (K x d): per-stratum effect vectors.}
\item{se_matrix}{Numeric matrix (K x d): per-stratum standard errors.}
\item{alpha}{Significance threshold. Vector Q uses alpha directly;
  scalar Q uses Bonferroni correction (alpha / d).}
}
\value{
A list with components:
\describe{
  \item{category}{One of "concordant_significant", "concordant_null",
    "rotation_only", or "component_only".}
  \item{vector_result}{Output from \code{\link{vector_sheaf_q_diagonal}}.}
  \item{scalar_results}{List of d outputs from \code{\link{scalar_cochran_q}}.}
  \item{rotation}{Output from \code{\link{max_rotation}}.}
}
}
\description{
Applies both the multivariate vector sheaf Q (diagonal covariance) and
per-trait scalar Cochran's Q with Bonferroni correction. Classification:
\itemize{
  \item \strong{concordant_significant}: both vector and at least one scalar test significant.
  \item \strong{concordant_null}: neither significant.
  \item \strong{rotation_only}: vector Q significant, no scalar Q significant after Bonferroni.
    Indicates effect vector rotation without per-trait magnitude changes.
  \item \strong{component_only}: at least one scalar Q significant, vector Q not.
}
}
\examples{
beta <- matrix(c(0.30, 0.10, 0.10, 0.30, 0.20, 0.20), nrow = 3, byrow = TRUE)
se <- matrix(0.04, nrow = 3, ncol = 2)
result <- classify_locus(beta, se)
result$category
}
