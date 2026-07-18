\name{simulate_pair}
\alias{simulate_pair}
\title{Generate a synthetic MR pair with known transportability status}
\usage{
simulate_pair(k = 4, beta_true = 0.3, tau = 0, se_range = c(0.03, 0.10),
              strata_prefix = "stratum", seed = NULL)
}
\arguments{
\item{k}{Number of strata.}
\item{beta_true}{True pooled causal effect.}
\item{tau}{Between-stratum standard deviation. Zero for transportable
  pairs, positive for non-transportable.}
\item{se_range}{Length-2 numeric vector: range of within-stratum
  standard errors (drawn uniformly).}
\item{strata_prefix}{Character prefix for stratum labels.}
\item{seed}{Optional integer seed for reproducibility. If NULL, no
  seed is set.}
}
\value{
A list with components:
\describe{
  \item{betas}{Numeric vector of observed per-stratum effects.}
  \item{ses}{Numeric vector of per-stratum standard errors.}
  \item{strata_names}{Character vector of stratum labels.}
  \item{ground_truth}{Either "transport" or "non-transport".}
  \item{params}{List with k, beta_true, tau.}
}
}
\description{
Creates a single exposure-outcome pair with \code{k} strata. When
\code{tau = 0}, all strata share the same true effect (transportable);
when \code{tau > 0}, true effects vary across strata (non-transportable).
}
\examples{
pair <- simulate_pair(k = 4, seed = 42)
pair$ground_truth  # "transport"
}
