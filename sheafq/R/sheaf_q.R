#' Standard Cochran's Q for scalar effect estimates
#'
#' @param betas Numeric vector of length K: per-stratum effect estimates.
#' @param ses Numeric vector of length K: per-stratum standard errors.
#' @return A list with components: Q, df, p, I2, tau2, beta_pooled.
#' @export
scalar_cochran_q <- function(betas, ses) {
  stopifnot(length(betas) == length(ses), length(betas) >= 2)
  w <- 1 / ses^2
  beta_bar <- sum(w * betas) / sum(w)
  Q <- sum(w * (betas - beta_bar)^2)
  df <- length(betas) - 1L
  p <- stats::pchisq(Q, df, lower.tail = FALSE)
  I2 <- if (Q > 0) max(0, (Q - df) / Q) else 0
  cc <- sum(w) - sum(w^2) / sum(w)
  tau2 <- if (cc > 0) max(0, (Q - df) / cc) else 0
  list(Q = Q, df = df, p = p, I2 = I2, tau2 = tau2, beta_pooled = beta_bar)
}


#' Multivariate sheaf Q for vector-valued stalks
#'
#' @param beta_matrix Numeric matrix (K x d): per-stratum effect vectors.
#' @param cov_matrices 3D array (K x d x d): per-stratum covariance matrices.
#' @return A list with components: Q_V, df, p, d, K.
#' @export
vector_sheaf_q <- function(beta_matrix, cov_matrices) {
  K <- nrow(beta_matrix)
  d <- ncol(beta_matrix)
  stopifnot(dim(cov_matrices)[1] == K,
            dim(cov_matrices)[2] == d,
            dim(cov_matrices)[3] == d)

  W_list <- lapply(seq_len(K), function(k) solve(cov_matrices[k, , ]))
  W_sum <- Reduce("+", W_list)
  W_sum_inv <- solve(W_sum)

  weighted_sum <- Reduce("+", lapply(seq_len(K), function(k) {
    W_list[[k]] %*% beta_matrix[k, ]
  }))
  beta_bar <- as.numeric(W_sum_inv %*% weighted_sum)

  Q_V <- 0
  for (k in seq_len(K)) {
    diff_k <- beta_matrix[k, ] - beta_bar
    Q_V <- Q_V + as.numeric(t(diff_k) %*% W_list[[k]] %*% diff_k)
  }

  df <- d * (K - 1L)
  p <- stats::pchisq(Q_V, df, lower.tail = FALSE)

  list(Q_V = Q_V, df = df, p = p, d = d, K = K)
}


#' Multivariate sheaf Q assuming diagonal per-stratum covariance
#'
#' Simpler interface when cross-trait correlations within each stratum
#' are unavailable. Each stratum's covariance is diag(se^2).
#'
#' @param beta_matrix Numeric matrix (K x d).
#' @param se_matrix Numeric matrix (K x d): per-stratum standard errors.
#' @return A list with components: Q_V, df, p, d, K, sum_scalar_Q.
#' @export
vector_sheaf_q_diagonal <- function(beta_matrix, se_matrix) {
  K <- nrow(beta_matrix)
  d <- ncol(beta_matrix)
  cov_matrices <- array(0, dim = c(K, d, d))
  for (k in seq_len(K)) {
    cov_matrices[k, , ] <- diag(se_matrix[k, ]^2, nrow = d)
  }

  result <- vector_sheaf_q(beta_matrix, cov_matrices)

  sum_scalar <- sum(vapply(seq_len(d), function(j) {
    scalar_cochran_q(beta_matrix[, j], se_matrix[, j])$Q
  }, numeric(1)))

  result$sum_scalar_Q <- sum_scalar
  result
}


#' Multivariate sheaf Q with within-stratum trait correlations
#'
#' In biobank data (same individuals, multiple traits), the within-stratum
#' covariance of effect estimates at a locus is:
#' Sigma_k[j,l] = rho_jl * SE_kj * SE_kl
#'
#' @param beta_matrix Numeric matrix (K x d).
#' @param se_matrix Numeric matrix (K x d).
#' @param rho_matrix Numeric matrix (d x d): phenotypic correlation matrix.
#' @return A list with components: Q_V, df, p, d, K, sum_scalar_Q.
#' @export
vector_sheaf_q_correlated <- function(beta_matrix, se_matrix, rho_matrix) {
  K <- nrow(beta_matrix)
  d <- ncol(beta_matrix)
  cov_matrices <- array(0, dim = c(K, d, d))
  for (k in seq_len(K)) {
    D_k <- diag(se_matrix[k, ], nrow = d)
    cov_matrices[k, , ] <- D_k %*% rho_matrix %*% D_k
  }

  result <- vector_sheaf_q(beta_matrix, cov_matrices)

  sum_scalar <- sum(vapply(seq_len(d), function(j) {
    scalar_cochran_q(beta_matrix[, j], se_matrix[, j])$Q
  }, numeric(1)))

  result$sum_scalar_Q <- sum_scalar
  result
}
