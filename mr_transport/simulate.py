"""Generate synthetic MR pairs with known ground truth for testing."""

from __future__ import annotations

from typing import Optional

import numpy as np


def simulate_pair(
    k: int = 4,
    beta_true: float = 0.3,
    tau: float = 0.0,
    se_range: tuple[float, float] = (0.03, 0.10),
    strata_prefix: str = "stratum",
    rng: Optional[np.random.Generator] = None,
) -> dict:
    """Generate a synthetic MR pair with known transportability status.

    Args:
        k: Number of strata.
        beta_true: True pooled causal effect.
        tau: Between-stratum SD. tau=0 means transportable (homogeneous);
            tau>0 means non-transportable (heterogeneous).
        se_range: Range of within-stratum SEs (drawn uniformly).
        strata_prefix: Label prefix for strata.
        rng: NumPy random generator.

    Returns:
        Dict with id, strata (beta, se, name), and ground_truth
        ("transport" if tau=0, else "non-transport").
    """
    if rng is None:
        rng = np.random.default_rng()

    ses = rng.uniform(se_range[0], se_range[1], size=k)
    if tau > 0:
        true_betas = beta_true + rng.normal(0, tau, size=k)
    else:
        true_betas = np.full(k, beta_true)
    observed_betas = true_betas + rng.normal(0, ses)

    strata = []
    for i in range(k):
        strata.append({
            "name": f"{strata_prefix}_{i+1}",
            "beta": float(observed_betas[i]),
            "se": float(ses[i]),
        })

    return {
        "strata": strata,
        "ground_truth": "non-transport" if tau > 0 else "transport",
        "params": {"k": k, "beta_true": beta_true, "tau": tau},
    }


def simulate_catalog(
    n_transport: int = 20,
    n_nontransport: int = 10,
    k_range: tuple[int, int] = (3, 6),
    tau_range: tuple[float, float] = (0.1, 0.5),
    seed: int = 42,
) -> list[dict]:
    """Generate a synthetic catalog of MR pairs with known labels.

    Produces n_transport homogeneous pairs (tau=0) and n_nontransport
    heterogeneous pairs (tau drawn from tau_range), with varying numbers
    of strata.

    Returns:
        List of pair dicts, each with strata, ground_truth, and params.
    """
    rng = np.random.default_rng(seed)
    pairs = []

    for i in range(n_transport):
        k = rng.integers(k_range[0], k_range[1] + 1)
        beta = rng.uniform(0.05, 0.5)
        pair = simulate_pair(k=k, beta_true=beta, tau=0.0, rng=rng)
        pair["id"] = f"synthetic_transport_{i+1}"
        pairs.append(pair)

    for i in range(n_nontransport):
        k = rng.integers(k_range[0], k_range[1] + 1)
        beta = rng.uniform(0.1, 0.8)
        tau = rng.uniform(tau_range[0], tau_range[1])
        pair = simulate_pair(k=k, beta_true=beta, tau=tau, rng=rng)
        pair["id"] = f"synthetic_nontransport_{i+1}"
        pairs.append(pair)

    return pairs
