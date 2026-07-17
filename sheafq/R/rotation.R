#' Angle between two vectors in degrees
#'
#' Returns 0-180 degrees. Returns NaN if either vector is zero.
#'
#' @param v1 Numeric vector.
#' @param v2 Numeric vector of same length.
#' @return Angle in degrees (scalar).
#' @export
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
#' @param beta_matrix Numeric matrix (K x d).
#' @return A list with components: theta_max, pair (indices of the two strata).
#' @export
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
