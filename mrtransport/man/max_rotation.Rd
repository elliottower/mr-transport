\name{max_rotation}
\alias{max_rotation}
\title{Maximum pairwise rotation angle across strata}
\usage{
max_rotation(beta_matrix)
}
\arguments{
\item{beta_matrix}{Numeric matrix (K x d): per-stratum effect vectors.}
}
\value{
A list with components:
\describe{
  \item{theta_max}{The maximum pairwise rotation angle in degrees.}
  \item{pair}{Integer vector of length 2: row indices of the two strata
    with the largest rotation.}
}
}
\description{
Computes the rotation angle between every pair of strata effect
vectors and returns the largest angle and the indices of the pair
that produced it.
}
\examples{
beta <- matrix(c(1, 0, 0, 1, 0.5, 0.5), nrow = 3, byrow = TRUE)
result <- max_rotation(beta)
result$theta_max   # 90
}
