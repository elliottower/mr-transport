#' Generate a synthetic MR pair with known transportability status
#'
#' Creates a single exposure-outcome pair with \code{k} strata. When
#' \code{transportable = TRUE} (tau = 0), all strata share the same
#' true effect; when \code{transportable = FALSE} (tau > 0), true
#' effects vary across strata.
#'
#' @param k Number of strata.
#' @param beta_true True pooled causal effect.
#' @param tau Between-stratum standard deviation. Zero for transportable
#'   pairs, positive for non-transportable.
#' @param se_range Length-2 numeric vector: range of within-stratum
#'   standard errors (drawn uniformly).
#' @param strata_prefix Character prefix for stratum labels.
#' @param seed Optional integer seed for reproducibility. If NULL, no
#'   seed is set.
#' @return A list with components:
#' \describe{
#'   \item{betas}{Numeric vector of observed per-stratum effects.}
#'   \item{ses}{Numeric vector of per-stratum standard errors.}
#'   \item{strata_names}{Character vector of stratum labels.}
#'   \item{ground_truth}{Either "transport" or "non-transport".}
#'   \item{params}{List with k, beta_true, tau.}
#' }
#' @export
#' @importFrom stats runif rnorm
#' @examples
#' pair <- simulate_pair(k = 4, seed = 42)
#' pair$ground_truth  # "transport"
simulate_pair <- function(k = 4L, beta_true = 0.3, tau = 0.0,
                          se_range = c(0.03, 0.10),
                          strata_prefix = "stratum",
                          seed = NULL) {
  if (!is.null(seed)) set.seed(seed)

  ses <- stats::runif(k, se_range[1], se_range[2])

  if (tau > 0) {
    true_betas <- beta_true + stats::rnorm(k, 0, tau)
  } else {
    true_betas <- rep(beta_true, k)
  }
  observed_betas <- true_betas + stats::rnorm(k, 0, ses)

  strata_names <- paste0(strata_prefix, "_", seq_len(k))

  ground_truth <- if (tau > 0) "non-transport" else "transport"

  list(
    betas = observed_betas,
    ses = ses,
    strata_names = strata_names,
    ground_truth = ground_truth,
    params = list(k = k, beta_true = beta_true, tau = tau)
  )
}


#' Generate a synthetic catalog of MR pairs with known labels
#'
#' Produces \code{n_transport} homogeneous pairs (tau = 0) and
#' \code{n_nontransport} heterogeneous pairs (tau drawn uniformly
#' from \code{tau_range}), with varying numbers of strata.
#'
#' @param n_transport Number of transportable pairs to generate.
#' @param n_nontransport Number of non-transportable pairs to generate.
#' @param k_range Length-2 integer vector: range of strata counts per pair.
#' @param tau_range Length-2 numeric vector: range of between-stratum
#'   SD for non-transportable pairs.
#' @param seed Integer seed for reproducibility.
#' @return A list of pair lists, each with components betas, ses,
#'   strata_names, ground_truth, id, and params.
#' @export
#' @importFrom stats runif rnorm
#' @examples
#' catalog <- simulate_catalog(n_transport = 5, n_nontransport = 3, seed = 42)
#' length(catalog)  # 8
simulate_catalog <- function(n_transport = 20L, n_nontransport = 10L,
                             k_range = c(3L, 6L),
                             tau_range = c(0.1, 0.5),
                             seed = 42L) {
  set.seed(seed)
  pairs <- list()

  for (i in seq_len(n_transport)) {
    k <- sample(k_range[1]:k_range[2], 1)
    beta <- stats::runif(1, 0.05, 0.5)
    pair <- simulate_pair(k = k, beta_true = beta, tau = 0.0)
    pair$id <- paste0("synthetic_transport_", i)
    pairs[[length(pairs) + 1L]] <- pair
  }

  for (i in seq_len(n_nontransport)) {
    k <- sample(k_range[1]:k_range[2], 1)
    beta <- stats::runif(1, 0.1, 0.8)
    tau <- stats::runif(1, tau_range[1], tau_range[2])
    pair <- simulate_pair(k = k, beta_true = beta, tau = tau)
    pair$id <- paste0("synthetic_nontransport_", i)
    pairs[[length(pairs) + 1L]] <- pair
  }

  pairs
}
