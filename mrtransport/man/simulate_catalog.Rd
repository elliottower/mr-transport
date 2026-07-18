\name{simulate_catalog}
\alias{simulate_catalog}
\title{Generate a synthetic catalog of MR pairs with known labels}
\usage{
simulate_catalog(n_transport = 20, n_nontransport = 10,
                 k_range = c(3, 6), tau_range = c(0.1, 0.5), seed = 42)
}
\arguments{
\item{n_transport}{Number of transportable pairs to generate.}
\item{n_nontransport}{Number of non-transportable pairs to generate.}
\item{k_range}{Length-2 integer vector: range of strata counts per pair.}
\item{tau_range}{Length-2 numeric vector: range of between-stratum
  SD for non-transportable pairs.}
\item{seed}{Integer seed for reproducibility.}
}
\value{
A list of pair lists, each with components betas, ses,
strata_names, ground_truth, id, and params.
}
\description{
Produces \code{n_transport} homogeneous pairs (tau = 0) and
\code{n_nontransport} heterogeneous pairs (tau drawn uniformly
from \code{tau_range}), with varying numbers of strata.
}
\examples{
catalog <- simulate_catalog(n_transport = 5, n_nontransport = 3, seed = 42)
length(catalog)  # 8
}
