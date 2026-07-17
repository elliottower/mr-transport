\name{rotation_angle}
\alias{rotation_angle}
\title{Angle between two vectors in degrees}
\usage{
rotation_angle(v1, v2)
}
\arguments{
\item{v1}{Numeric vector.}
\item{v2}{Numeric vector of same length as v1.}
}
\value{
Angle in degrees (0 to 180). Returns NaN if either vector is zero.
}
\description{
Computes the angle between two effect vectors using the arccosine of their
normalized dot product. Useful for quantifying effect vector rotation between
two population strata.
}
\examples{
rotation_angle(c(1, 0), c(0, 1))  # 90
rotation_angle(c(1, 0), c(1, 0))  # 0
rotation_angle(c(1, 1), c(-1, 1)) # 90
}
