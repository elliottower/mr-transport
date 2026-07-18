\name{alpha_sweep}
\alias{alpha_sweep}
\title{Sweep significance thresholds and report verdict at each}
\usage{
alpha_sweep(betas, ses,
            alphas = c(0.001, 0.005, 0.01, 0.025, 0.05, 0.075, 0.10, 0.15, 0.20))
}
\arguments{
\item{betas}{Numeric vector of per-stratum effect estimates.}
\item{ses}{Numeric vector of per-stratum standard errors.}
\item{alphas}{Numeric vector of significance thresholds to test.}
}
\value{
A data.frame with columns:
\describe{
  \item{alpha}{The significance threshold.}
  \item{verdict}{Either "transport" or "non-transport".}
  \item{Q}{Cochran's Q statistic (constant across rows).}
  \item{p}{P-value (constant across rows).}
  \item{power}{Post-hoc power at this alpha level.}
}
}
\description{
Runs \code{\link{test_transport}} at each alpha level to show how
the verdict and power change across a range of thresholds. Useful for
assessing how sensitive the transportability conclusion is to the
choice of significance level.
}
\examples{
sweep <- alpha_sweep(
  betas = c(0.25, 0.23, 0.28),
  ses = c(0.05, 0.06, 0.07)
)
sweep
}
