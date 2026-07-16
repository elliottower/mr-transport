"""Sensitivity analyses: LOO, alpha sweep, random-effects comparison."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
from scipy.stats import chi2

from mr_transport.core import _cochran_q, test_transport


@dataclass(frozen=True)
class LOOResult:
    """Leave-one-out stability result for one pair."""

    stable: bool
    flipped_strata: list[str]


def leave_one_out(
    betas: Sequence[float],
    ses: Sequence[float],
    strata_names: Sequence[str],
    alpha: float = 0.05,
) -> LOOResult:
    """Check if classification is stable when dropping each stratum in turn."""
    betas_arr = np.asarray(betas, dtype=np.float64)
    ses_arr = np.asarray(ses, dtype=np.float64)
    names = list(strata_names)

    if len(betas_arr) <= 2:
        return LOOResult(stable=True, flipped_strata=[])

    full = _cochran_q(betas_arr, ses_arr)
    full_verdict = "non-transport" if full["p"] < alpha else "transport"

    flipped = []
    for i in range(len(betas_arr)):
        sub_b = np.delete(betas_arr, i)
        sub_s = np.delete(ses_arr, i)
        sub = _cochran_q(sub_b, sub_s)
        sub_verdict = "non-transport" if sub["p"] < alpha else "transport"
        if sub_verdict != full_verdict:
            flipped.append(names[i])

    return LOOResult(stable=len(flipped) == 0, flipped_strata=flipped)


def alpha_sweep(
    betas: Sequence[float],
    ses: Sequence[float],
    alphas: Sequence[float] = (0.001, 0.005, 0.01, 0.025, 0.05, 0.075, 0.10, 0.15, 0.20),
) -> list[dict]:
    """Sweep alpha thresholds and return verdict + power at each."""
    results = []
    for a in alphas:
        r = test_transport(betas, ses, alpha=a)
        results.append({"alpha": a, "verdict": r.verdict, "Q": r.Q, "p": r.p, "power": r.power})
    return results


def random_effects(
    betas: Sequence[float],
    ses: Sequence[float],
) -> dict:
    """DerSimonian-Laird random-effects comparison."""
    betas_arr = np.asarray(betas, dtype=np.float64)
    ses_arr = np.asarray(ses, dtype=np.float64)
    w = 1.0 / (ses_arr**2)
    beta_fe = float(np.sum(w * betas_arr) / np.sum(w))
    se_fe = float(1.0 / np.sqrt(np.sum(w)))

    k = len(betas_arr)
    df = k - 1
    Q = float(np.sum(w * (betas_arr - beta_fe) ** 2))
    C = float(np.sum(w) - np.sum(w**2) / np.sum(w))
    tau2 = float(max(0.0, (Q - df) / C)) if C > 0 else 0.0
    I2 = float(max(0.0, (Q - df) / Q)) if Q > 0 else 0.0

    w_re = 1.0 / (ses_arr**2 + tau2)
    beta_re = float(np.sum(w_re * betas_arr) / np.sum(w_re))
    se_re = float(1.0 / np.sqrt(np.sum(w_re)))

    return {
        "beta_fe": beta_fe,
        "se_fe": se_fe,
        "beta_re": beta_re,
        "se_re": se_re,
        "beta_shift": abs(beta_re - beta_fe),
        "se_ratio": se_re / se_fe if se_fe > 0 else 1.0,
        "tau2": tau2,
        "I2": I2,
    }
