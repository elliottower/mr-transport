#' Classify a locus as concordant, rotation-only, or component-only
#'
#' Applies both vector sheaf Q (diagonal covariance) and per-trait scalar Q
#' with Bonferroni correction, then classifies based on which tests are
#' significant.
#'
#' @param beta_matrix Numeric matrix (K x d).
#' @param se_matrix Numeric matrix (K x d).
#' @param alpha Significance threshold (before Bonferroni correction for scalar tests).
#' @return A list with components: category, vector_result, scalar_results, rotation.
#' @export
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
