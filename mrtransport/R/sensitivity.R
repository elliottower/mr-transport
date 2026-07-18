#' Leave-one-out stability check for transportability verdict
#'
#' Drops each stratum in turn and re-runs the Q test, checking whether
#' the verdict changes. If the full-data verdict flips when any single
#' stratum is removed, the result is flagged as unstable and the
#' influential strata are listed.
#'
#' @param betas Numeric vector of per-stratum effect estimates.
#' @param ses Numeric vector of per-stratum standard errors.
#' @param strata_names Character vector of stratum labels.
#' @param alpha Significance threshold.
#' @return A list with components:
#' \describe{
#'   \item{stable}{Logical: TRUE if the verdict does not change when any
#'     single stratum is dropped.}
#'   \item{flipped_strata}{Character vector of stratum names whose removal
#'     changes the verdict (empty if stable).}
#' }
#' @export
#' @importFrom stats pchisq
#' @examples
#' loo <- leave_one_out(
#'   betas = c(0.25, 0.23, 0.28),
#'   ses = c(0.05, 0.06, 0.07),
#'   strata_names = c("EUR", "EAS", "AFR")
#' )
#' loo$stable
leave_one_out <- function(betas, ses, strata_names, alpha = 0.05) {
  stopifnot(length(betas) == length(ses))
  stopifnot(length(betas) == length(strata_names))

  if (length(betas) <= 2) {
    return(list(stable = TRUE, flipped_strata = character(0)))
  }

  full <- scalar_cochran_q(betas, ses)
  full_verdict <- if (full$p < alpha) "non-transport" else "transport"

  flipped <- character(0)
  for (i in seq_along(betas)) {
    sub <- scalar_cochran_q(betas[-i], ses[-i])
    sub_verdict <- if (sub$p < alpha) "non-transport" else "transport"
    if (sub_verdict != full_verdict) {
      flipped <- c(flipped, strata_names[i])
    }
  }

  list(stable = length(flipped) == 0, flipped_strata = flipped)
}


#' Sweep significance thresholds and report verdict at each
#'
#' Runs \code{\link{test_transport}} at each alpha level to show how
#' the verdict and power change across a range of thresholds.
#'
#' @param betas Numeric vector of per-stratum effect estimates.
#' @param ses Numeric vector of per-stratum standard errors.
#' @param alphas Numeric vector of significance thresholds to test.
#' @return A data.frame with columns: alpha, verdict, Q, p, power.
#' @export
#' @examples
#' sweep <- alpha_sweep(
#'   betas = c(0.25, 0.23, 0.28),
#'   ses = c(0.05, 0.06, 0.07)
#' )
#' sweep
alpha_sweep <- function(betas, ses,
                        alphas = c(0.001, 0.005, 0.01, 0.025, 0.05,
                                   0.075, 0.10, 0.15, 0.20)) {
  rows <- lapply(alphas, function(a) {
    r <- test_transport(betas, ses, alpha = a)
    data.frame(
      alpha = a,
      verdict = r$verdict,
      Q = r$Q,
      p = r$p,
      power = r$power,
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, rows)
}
