\name{transport_power}
\alias{transport_power}
\title{Compute post-hoc power for a Cochran's Q test}
\usage{
transport_power(Q, df, alpha = 0.05)
}
\arguments{
\item{Q}{Observed Cochran's Q statistic.}
\item{df}{Degrees of freedom (k - 1).}
\item{alpha}{Significance threshold.}
}
\value{
Power (numeric scalar between 0 and 1).
}
\description{
Uses the noncentral chi-squared distribution to estimate the probability
of rejecting the null hypothesis given the observed Q statistic. The
noncentrality parameter is \code{max(0, Q - df)}.
}
\examples{
transport_power(15, 3, 0.05)  # high power
transport_power(3, 3, 0.05)   # power = alpha (no signal)
}
