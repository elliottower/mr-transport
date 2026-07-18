\name{strata_needed}
\alias{strata_needed}
\title{Estimate number of strata needed to detect heterogeneity}
\usage{
strata_needed(I2, target_power = 0.80, alpha = 0.05, max_k = 50)
}
\arguments{
\item{I2}{Assumed or observed I-squared value (between 0 and 1).}
\item{target_power}{Desired power level.}
\item{alpha}{Significance threshold.}
\item{max_k}{Maximum number of strata to consider.}
}
\value{
Integer number of strata needed, or NULL if \code{max_k} strata
are insufficient.
}
\description{
Given an observed or assumed I-squared value, estimates how many
equally-weighted strata would be needed for the Q test to achieve
the target power. The noncentrality parameter is computed as
\code{lam = df * I2 / (1 - I2)}.
}
\examples{
strata_needed(I2 = 0.58, target_power = 0.80)
strata_needed(I2 = 0.10, target_power = 0.80)  # may need many strata
}
