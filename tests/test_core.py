import numpy as np
import pytest
from scipy.stats import chi2

from mr_transport.core import TransportResult, _cochran_q, _power, strata_needed
from mr_transport.core import test_transport as run_transport


class TestCochranQAnalytical:
    def test_perfect_homogeneity_gives_zero_q(self):
        betas = np.array([0.3, 0.3, 0.3, 0.3])
        ses = np.array([0.05, 0.08, 0.06, 0.10])
        stats = _cochran_q(betas, ses)
        assert stats["Q"] == pytest.approx(0.0, abs=1e-12)
        assert stats["p"] == pytest.approx(1.0, abs=1e-10)
        assert stats["I2"] == pytest.approx(0.0, abs=1e-12)
        assert stats["tau2"] == pytest.approx(0.0, abs=1e-12)
        assert stats["beta_pooled"] == pytest.approx(0.3, abs=1e-10)

    def test_two_strata_equal_se_analytical_q(self):
        a, b, s = 0.5, 0.2, 0.04
        expected_q = (a - b) ** 2 / (2 * s**2)
        betas = np.array([a, b])
        ses = np.array([s, s])
        stats = _cochran_q(betas, ses)
        assert stats["Q"] == pytest.approx(expected_q, rel=1e-10)
        assert stats["df"] == 1
        expected_p = 1.0 - chi2.cdf(expected_q, 1)
        assert stats["p"] == pytest.approx(expected_p, rel=1e-8)

    def test_pooled_beta_is_inverse_variance_weighted(self):
        betas = np.array([0.1, 0.5])
        ses = np.array([0.01, 0.10])
        w = 1.0 / ses**2
        expected = np.sum(w * betas) / np.sum(w)
        stats = _cochran_q(betas, ses)
        assert stats["beta_pooled"] == pytest.approx(expected, rel=1e-10)

    def test_i2_bounded_zero_one(self):
        rng = np.random.default_rng(None)
        for _ in range(200):
            k = rng.integers(2, 10)
            betas = rng.normal(0, 1, size=k)
            ses = rng.uniform(0.01, 0.5, size=k)
            stats = _cochran_q(betas, ses)
            assert 0.0 <= stats["I2"] <= 1.0

    def test_tau2_nonnegative(self):
        rng = np.random.default_rng(None)
        for _ in range(200):
            k = rng.integers(2, 10)
            betas = rng.normal(0, 1, size=k)
            ses = rng.uniform(0.01, 0.5, size=k)
            stats = _cochran_q(betas, ses)
            assert stats["tau2"] >= 0.0


class TestPower:
    def test_power_at_null_equals_alpha(self):
        for alpha in [0.01, 0.05, 0.10]:
            pw = _power(Q=3.0, df=3, alpha=alpha)
            assert pw == pytest.approx(alpha, abs=0.001)

    def test_power_increases_with_noncentrality(self):
        powers = [_power(Q=5 + lam, df=5, alpha=0.05) for lam in [0, 5, 10, 20, 50]]
        for i in range(len(powers) - 1):
            assert powers[i] <= powers[i + 1] + 1e-10

    def test_power_bounded_zero_one(self):
        rng = np.random.default_rng(None)
        for _ in range(200):
            df = rng.integers(1, 20)
            Q = rng.uniform(0, 100)
            pw = _power(Q, df, alpha=0.05)
            assert 0.0 <= pw <= 1.0


class TestTestTransport:
    def test_homogeneous_verdict_is_transport(self):
        r = run_transport([0.3, 0.3, 0.3, 0.3], [0.05, 0.08, 0.06, 0.10])
        assert r.verdict == "transport"
        assert r.is_transportable is True
        assert r.Q == pytest.approx(0.0, abs=1e-10)
        assert r.I2 == pytest.approx(0.0, abs=1e-10)

    def test_highly_heterogeneous_verdict_is_nontransport(self):
        r = run_transport([1.6, 0.2, -0.5], [0.02, 0.02, 0.02])
        assert r.verdict == "non-transport"
        assert r.is_transportable is False
        assert r.p < 0.001

    def test_lists_and_arrays_give_identical_results(self):
        betas_list = [0.4, 0.1, 0.35, 0.2]
        ses_list = [0.05, 0.06, 0.04, 0.08]
        r_list = run_transport(betas_list, ses_list)
        r_arr = run_transport(np.array(betas_list), np.array(ses_list))
        assert r_list.Q == pytest.approx(r_arr.Q)
        assert r_list.p == pytest.approx(r_arr.p)
        assert r_list.verdict == r_arr.verdict

    def test_strata_names_propagated(self):
        names = ["EUR", "EAS", "AFR"]
        r = run_transport([0.3, 0.3, 0.3], [0.05, 0.05, 0.05], strata_names=names)
        assert r.strata_names == names

    def test_strata_names_default_none(self):
        r = run_transport([0.3, 0.3], [0.05, 0.05])
        assert r.strata_names is None

    def test_k_matches_input_length(self):
        for k in [2, 5, 10]:
            r = run_transport([0.3] * k, [0.05] * k)
            assert r.k == k

    def test_custom_alpha_changes_verdict_threshold(self):
        betas = [0.3, 0.1, 0.25, 0.15]
        ses = [0.05, 0.06, 0.04, 0.08]
        r_strict = run_transport(betas, ses, alpha=0.001)
        r_loose = run_transport(betas, ses, alpha=0.50)
        assert r_strict.p == pytest.approx(r_loose.p)
        if r_strict.verdict == "non-transport":
            assert r_loose.verdict == "non-transport"


class TestTransportResultProperties:
    def test_is_transportable_matches_verdict(self):
        rng = np.random.default_rng(None)
        for _ in range(100):
            k = rng.integers(3, 8)
            betas = rng.normal(0.3, 0.3, size=k)
            ses = rng.uniform(0.02, 0.1, size=k)
            r = run_transport(betas.tolist(), ses.tolist())
            assert r.is_transportable == (r.verdict == "transport")

    def test_underpowered_requires_transport_low_power_high_i2(self):
        r_transport_low_power = TransportResult(
            Q=5.0, df=3, p=0.17, I2=0.40, tau2=0.01,
            power=0.30, verdict="transport", beta_pooled=0.3, k=4, strata_names=None,
        )
        assert r_transport_low_power.underpowered is True

        r_nontransport = TransportResult(
            Q=20.0, df=3, p=0.001, I2=0.85, tau2=0.05,
            power=0.30, verdict="non-transport", beta_pooled=0.3, k=4, strata_names=None,
        )
        assert r_nontransport.underpowered is False

        r_high_power = TransportResult(
            Q=5.0, df=3, p=0.17, I2=0.40, tau2=0.01,
            power=0.80, verdict="transport", beta_pooled=0.3, k=4, strata_names=None,
        )
        assert r_high_power.underpowered is False

        r_low_i2 = TransportResult(
            Q=1.0, df=3, p=0.80, I2=0.10, tau2=0.001,
            power=0.10, verdict="transport", beta_pooled=0.3, k=4, strata_names=None,
        )
        assert r_low_i2.underpowered is False

    def test_repr_contains_key_fields(self):
        r = run_transport([0.3, 0.3, 0.3], [0.05, 0.05, 0.05])
        s = repr(r)
        assert "verdict=" in s
        assert "Q=" in s
        assert "power=" in s


class TestInputValidation:
    def test_length_mismatch_raises(self):
        with pytest.raises(ValueError, match="same length"):
            run_transport([0.3, 0.2], [0.05])

    def test_fewer_than_two_strata_raises(self):
        with pytest.raises(ValueError, match="at least 2"):
            run_transport([0.3], [0.05])

    def test_nonpositive_se_raises(self):
        with pytest.raises(ValueError, match="positive"):
            run_transport([0.3, 0.2], [0.05, 0.0])
        with pytest.raises(ValueError, match="positive"):
            run_transport([0.3, 0.2], [0.05, -0.01])


class TestStrataNeeded:
    def test_returns_two_for_extreme_heterogeneity(self):
        assert strata_needed(I2=0.99) == 2

    def test_returns_none_for_zero_heterogeneity(self):
        assert strata_needed(I2=0.0) is None

    def test_monotonically_decreasing_in_i2(self):
        i2_values = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]
        results = [strata_needed(i2) for i2 in i2_values]
        for i in range(len(results) - 1):
            if results[i] is not None and results[i + 1] is not None:
                assert results[i] >= results[i + 1]

    def test_respects_target_power(self):
        k_low = strata_needed(I2=0.5, target_power=0.50)
        k_high = strata_needed(I2=0.5, target_power=0.95)
        assert k_low is not None
        assert k_high is not None
        assert k_low <= k_high

    def test_respects_max_k(self):
        result = strata_needed(I2=0.05, max_k=5)
        assert result is None or result <= 5
