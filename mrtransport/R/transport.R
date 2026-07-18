#' Compute post-hoc power for a Cochran's Q test
#'
#' Uses the noncentral chi-squared distribution to estimate the probability
#' of rejecting the null hypothesis given the observed Q statistic.
#'
#' @param Q Observed Cochran's Q statistic.
#' @param df Degrees of freedom (k - 1).
#' @param alpha Significance threshold.
#' @return Power (numeric scalar between 0 and 1).
#' @export
#' @importFrom stats pchisq qchisq
transport_power <- function(Q, df, alpha = 0.05) {
  lam <- max(0, Q - df)
  if (lam == 0) return(alpha)
  crit <- stats::qchisq(1 - alpha, df)
  stats::pchisq(crit, df, ncp = lam, lower.tail = FALSE)
}


#' Test whether stratified MR estimates are transportable
#'
#' Runs Cochran's Q heterogeneity test on a set of per-stratum causal effect
#' estimates, computes post-hoc power, and returns a verdict of "transport"
#' (Q not significant) or "non-transport" (Q significant at level alpha).
#'
#' @param betas Numeric vector of per-stratum causal effect estimates
#'   (log-OR or beta scale).
#' @param ses Numeric vector of per-stratum standard errors, same length
#'   as \code{betas}.
#' @param strata_names Optional character vector of stratum labels (e.g.
#'   ancestry names). If NULL, strata are unnamed.
#' @param alpha Significance threshold for the Q test.
#' @return A list with components:
#' \describe{
#'   \item{Q}{Cochran's Q statistic.}
#'   \item{df}{Degrees of freedom (k - 1).}
#'   \item{p}{P-value from the chi-squared distribution.}
#'   \item{I2}{I-squared heterogeneity measure (0 to 1).}
#'   \item{tau2}{DerSimonian-Laird between-stratum variance estimate.}
#'   \item{power}{Post-hoc power of the Q test.}
#'   \item{verdict}{Either "transport" or "non-transport".}
#'   \item{beta_pooled}{Inverse-variance weighted pooled estimate.}
#'   \item{k}{Number of strata.}
#'   \item{strata_names}{Character vector of stratum labels or NULL.}
#'   \item{is_transportable}{Logical: TRUE if verdict is "transport".}
#'   \item{underpowered}{Logical: TRUE if verdict is "transport" but
#'     power < 0.50 and I2 > 0.30.}
#' }
#' @export
#' @examples
#' result <- test_transport(
#'   betas = c(1.6, 1.2, 0.8, 1.0),
#'   ses = c(0.04, 0.07, 0.12, 0.10),
#'   strata_names = c("EUR", "EAS", "AFR", "HISP")
#' )
#' result$verdict   # "non-transport"
#' result$power     # high
test_transport <- function(betas, ses, strata_names = NULL, alpha = 0.05) {
  stopifnot(length(betas) == length(ses))
  stopifnot(length(betas) >= 2)
  stopifnot(all(ses > 0))

  stats <- scalar_cochran_q(betas, ses)
  power <- transport_power(stats$Q, stats$df, alpha)
  verdict <- if (stats$p < alpha) "non-transport" else "transport"
  is_transportable <- verdict == "transport"
  underpowered <- is_transportable && power < 0.50 && stats$I2 > 0.30

  list(
    Q = stats$Q,
    df = stats$df,
    p = stats$p,
    I2 = stats$I2,
    tau2 = stats$tau2,
    power = power,
    verdict = verdict,
    beta_pooled = stats$beta_pooled,
    k = length(betas),
    strata_names = strata_names,
    is_transportable = is_transportable,
    underpowered = underpowered
  )
}


#' Estimate number of strata needed to detect heterogeneity
#'
#' Given an observed or assumed I-squared value, estimates how many
#' equally-weighted strata would be needed for the Q test to achieve
#' the target power.
#'
#' @param I2 Assumed or observed I-squared value (between 0 and 1).
#' @param target_power Desired power level.
#' @param alpha Significance threshold.
#' @param max_k Maximum number of strata to consider.
#' @return Integer number of strata needed, or NULL if \code{max_k}
#'   strata are insufficient.
#' @export
#' @importFrom stats pchisq qchisq
#' @examples
#' strata_needed(I2 = 0.58, target_power = 0.80)
strata_needed <- function(I2, target_power = 0.80, alpha = 0.05, max_k = 50L) {
  if (I2 <= 0) return(NULL)
  if (I2 >= 1.0) return(2L)
  for (k in 2:max_k) {
    df <- k - 1L
    lam <- df * I2 / (1 - I2)
    crit <- stats::qchisq(1 - alpha, df)
    pw <- stats::pchisq(crit, df, ncp = lam, lower.tail = FALSE)
    if (pw >= target_power) return(k)
  }
  NULL
}
