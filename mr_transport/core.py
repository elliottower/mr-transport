"""Core transportability test: Cochran's Q + power + verdict."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

import numpy as np
from scipy.stats import chi2, ncx2


@dataclass(frozen=True)
class TransportResult:
    """Result of a single transportability test."""

    Q: float
    df: int
    p: float
    I2: float
    tau2: float
    power: float
    verdict: str
    beta_pooled: float
    k: int
    strata_names: Optional[list[str]]

    def __repr__(self) -> str:
        return (
            f"TransportResult(verdict={self.verdict!r}, Q={self.Q:.3f}, "
            f"p={self.p:.2e}, I²={self.I2:.1%}, power={self.power:.2f}, k={self.k})"
        )

    @property
    def is_transportable(self) -> bool:
        return self.verdict == "transport"

    @property
    def underpowered(self) -> bool:
        return self.verdict == "transport" and self.power < 0.50 and self.I2 > 0.30


def _cochran_q(betas: np.ndarray, ses: np.ndarray) -> dict:
    w = 1.0 / (ses**2)
    beta_pooled = float(np.sum(w * betas) / np.sum(w))
    Q = float(np.sum(w * (betas - beta_pooled) ** 2))
    k = len(betas)
    df = k - 1
    p = float(1.0 - chi2.cdf(Q, df))
    I2 = float(max(0.0, (Q - df) / Q)) if Q > 0 else 0.0
    C = float(np.sum(w) - np.sum(w**2) / np.sum(w))
    tau2 = float(max(0.0, (Q - df) / C)) if C > 0 else 0.0
    return {"Q": Q, "df": df, "p": p, "I2": I2, "tau2": tau2, "beta_pooled": beta_pooled, "k": k}


def _power(Q: float, df: int, alpha: float) -> float:
    lam = max(0.0, Q - df)
    if lam == 0.0:
        return alpha
    crit = chi2.ppf(1 - alpha, df)
    return float(1.0 - ncx2.cdf(crit, df, lam))


def test_transport(
    betas: Sequence[float],
    ses: Sequence[float],
    strata_names: Optional[Sequence[str]] = None,
    alpha: float = 0.05,
) -> TransportResult:
    """Test whether a set of stratified MR estimates are transportable.

    Args:
        betas: Per-stratum causal effect estimates (log-OR or beta scale).
        ses: Per-stratum standard errors, same length as betas.
        strata_names: Optional labels for each stratum (e.g. ancestry).
        alpha: Significance threshold for the Q test.

    Returns:
        TransportResult with Q statistic, p-value, I², power, and verdict.
    """
    betas_arr = np.asarray(betas, dtype=np.float64)
    ses_arr = np.asarray(ses, dtype=np.float64)
    if len(betas_arr) != len(ses_arr):
        raise ValueError(f"betas ({len(betas_arr)}) and ses ({len(ses_arr)}) must have same length")
    if len(betas_arr) < 2:
        raise ValueError(f"Need at least 2 strata, got {len(betas_arr)}")
    if np.any(ses_arr <= 0):
        raise ValueError("All standard errors must be positive")

    stats = _cochran_q(betas_arr, ses_arr)
    power = _power(stats["Q"], stats["df"], alpha)
    verdict = "non-transport" if stats["p"] < alpha else "transport"

    names = list(strata_names) if strata_names is not None else None
    return TransportResult(
        Q=stats["Q"],
        df=stats["df"],
        p=stats["p"],
        I2=stats["I2"],
        tau2=stats["tau2"],
        power=power,
        verdict=verdict,
        beta_pooled=stats["beta_pooled"],
        k=stats["k"],
        strata_names=names,
    )


def strata_needed(
    I2: float,
    target_power: float = 0.80,
    alpha: float = 0.05,
    max_k: int = 50,
) -> Optional[int]:
    """Estimate the number of strata needed to detect heterogeneity at target power.

    Given an observed or assumed I² value, estimates how many equally-weighted
    strata would be needed for the Q test to achieve the target power.

    Returns None if max_k strata are insufficient.
    """
    if I2 <= 0:
        return None
    if I2 >= 1.0:
        return 2
    for k in range(2, max_k + 1):
        df = k - 1
        lam = df * I2 / (1.0 - I2)
        crit = chi2.ppf(1 - alpha, df)
        pw = float(1.0 - ncx2.cdf(crit, df, lam))
        if pw >= target_power:
            return k
    return None
