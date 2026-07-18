#' Classify a locus as concordant, rotation-only, or component-only
#'
#' Applies both the multivariate vector sheaf Q (diagonal covariance) and
#' per-trait scalar Cochran's Q with Bonferroni correction. Classification:
#' \itemize{
#'   \item \strong{concordant_significant}: both vector and at least one
#'     scalar test significant.
#'   \item \strong{concordant_null}: neither significant.
#'   \item \strong{rotation_only}: vector Q significant, no scalar Q
#'     significant after Bonferroni. Indicates effect vector rotation
#'     without per-trait magnitude changes.
#'   \item \strong{component_only}: at least one scalar Q significant,
#'     vector Q not.
#' }
#'
#' @param beta_matrix Numeric matrix (K x d): per-stratum effect vectors.
#' @param se_matrix Numeric matrix (K x d): per-stratum standard errors.
#' @param alpha Significance threshold. Vector Q uses alpha directly;
#'   scalar Q uses Bonferroni correction (alpha / d).
#' @return A list with components:
#' \describe{
#'   \item{category}{One of "concordant_significant", "concordant_null",
#'     "rotation_only", or "component_only".}
#'   \item{vector_result}{Output from \code{\link{vector_sheaf_q_diagonal}}.}
#'   \item{scalar_results}{List of d outputs from
#'     \code{\link{scalar_cochran_q}}.}
#'   \item{rotation}{Output from \code{\link{max_rotation}}.}
#' }
#' @export
#' @examples
#' beta <- matrix(c(0.30, 0.10, 0.10, 0.30, 0.20, 0.20),
#'                nrow = 3, byrow = TRUE)
#' se <- matrix(0.04, nrow = 3, ncol = 2)
#' result <- classify_locus(beta, se)
#' result$category
classify_locus <- function(beta_matrix, se_matrix, alpha = 0.05) {
  K <- nrow(beta_matrix)
  d <- ncol(beta_matrix)

  vector_result <- vector_sheaf_q_diagonal(beta_matrix, se_matrix)

  scalar_results <- lapply(seq_len(d), function(j) {
    scalar_cochran_q(beta_matrix[, j], se_matrix[, j])
  })

  alpha_bonf <- alpha / d
  any_scalar_sig <- any(vapply(scalar_results, function(r) r$p < alpha_bonf, logical(1)))
  vector_sig <- vector_result$p < alpha

  category <- if (vector_sig && any_scalar_sig) {
    "concordant_significant"
  } else if (!vector_sig && !any_scalar_sig) {
    "concordant_null"
  } else if (vector_sig && !any_scalar_sig) {
    "rotation_only"
  } else {
    "component_only"
  }

  rot <- max_rotation(beta_matrix)

  list(
    category = category,
    vector_result = vector_result,
    scalar_results = scalar_results,
    rotation = rot
  )
}
