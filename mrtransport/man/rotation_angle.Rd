\name{rotation_angle}
\alias{rotation_angle}
\title{Angle between two vectors in degrees}
\usage{
rotation_angle(v1, v2)
}
\arguments{
\item{v1}{Numeric vector.}
\item{v2}{Numeric vector of same length as \code{v1}.}
}
\value{
Angle in degrees (scalar between 0 and 180). NaN if either vector is zero.
}
\description{
Computes the angle between two numeric vectors using the dot product
formula. Returns a value between 0 and 180 degrees, or NaN if either
vector has zero norm.
}
\examples{
rotation_angle(c(1, 0), c(0, 1))   # 90
rotation_angle(c(1, 0), c(1, 0))   # 0
rotation_angle(c(1, 0), c(-1, 0))  # 180
}
