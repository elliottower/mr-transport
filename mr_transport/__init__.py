"""mr-transport: MR transportability classification via Cochran's Q with power analysis."""

from mr_transport.core import (
    TransportResult,
    test_transport,
    strata_needed,
)
from mr_transport.catalog import load_catalog
from mr_transport.simulate import simulate_pair, simulate_catalog

__version__ = "0.1.0"

__all__ = [
    "TransportResult",
    "test_transport",
    "strata_needed",
    "load_catalog",
    "simulate_pair",
    "simulate_catalog",
]
