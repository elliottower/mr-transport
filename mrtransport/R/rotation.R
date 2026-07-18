#' Angle between two vectors in degrees
#'
#' Computes the angle between two numeric vectors using the dot product
#' formula. Returns a value between 0 and 180 degrees, or NaN if either
#' vector has zero norm.
#'
#' @param v1 Numeric vector.
#' @param v2 Numeric vector of same length as \code{v1}.
#' @return Angle in degrees (scalar). NaN if either vector is zero.
#' @export
#' @examples
#' rotation_angle(c(1, 0), c(0, 1))   # 90
#' rotation_angle(c(1, 0), c(1, 0))   # 0
rotation_angle <- function(v1, v2) {
  stopifnot(length(v1) == length(v2))
  n1 <- sqrt(sum(v1^2))
  n2 <- sqrt(sum(v2^2))
  if (n1 < 1e-12 || n2 < 1e-12) return(NaN)
  cos_theta <- max(-1, min(1, sum(v1 * v2) / (n1 * n2)))
  acos(cos_theta) * 180 / pi
}


#' Maximum pairwise rotation angle across strata
#'
#' Computes the rotation angle between every pair of strata effect
#' vectors and returns the largest angle and the indices of the pair
#' that produced it.
#'
#' @param beta_matrix Numeric matrix (K x d): per-stratum effect vectors.
#' @return A list with components:
#' \describe{
#'   \item{theta_max}{The maximum pairwise rotation angle in degrees.}
#'   \item{pair}{Integer vector of length 2: row indices of the two strata
#'     with the largest rotation.}
#' }
#' @export
#' @examples
#' beta <- matrix(c(1, 0, 0, 1, 0.5, 0.5), nrow = 3, byrow = TRUE)
#' result <- max_rotation(beta)
#' result$theta_max   # 90
max_rotation <- function(beta_matrix) {
  K <- nrow(beta_matrix)
  theta_max <- 0
  pair <- c(1L, 1L)
  for (i in seq_len(K - 1L)) {
    for (j in (i + 1L):K) {
      theta <- rotation_angle(beta_matrix[i, ], beta_matrix[j, ])
      if (!is.nan(theta) && theta > theta_max) {
        theta_max <- theta
        pair <- c(i, j)
      }
    }
  }
  list(theta_max = theta_max, pair = pair)
}
