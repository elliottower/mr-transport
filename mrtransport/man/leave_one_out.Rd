\name{leave_one_out}
\alias{leave_one_out}
\title{Leave-one-out stability check for transportability verdict}
\usage{
leave_one_out(betas, ses, strata_names, alpha = 0.05)
}
\arguments{
\item{betas}{Numeric vector of per-stratum effect estimates.}
\item{ses}{Numeric vector of per-stratum standard errors.}
\item{strata_names}{Character vector of stratum labels.}
\item{alpha}{Significance threshold.}
}
\value{
A list with components:
\describe{
  \item{stable}{Logical: TRUE if the verdict does not change when any
    single stratum is dropped.}
  \item{flipped_strata}{Character vector of stratum names whose removal
    changes the verdict (empty if stable).}
}
}
\description{
Drops each stratum in turn and re-runs the Q test, checking whether
the verdict changes. If the full-data verdict flips when any single
stratum is removed, the result is flagged as unstable and the
influential strata are listed.
}
\examples{
loo <- leave_one_out(
  betas = c(0.25, 0.23, 0.28),
  ses = c(0.05, 0.06, 0.07),
  strata_names = c("EUR", "EAS", "AFR")
)
loo$stable
}
