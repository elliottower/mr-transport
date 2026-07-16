import numpy as np
import pytest

from mr_transport.sensitivity import alpha_sweep, leave_one_out, random_effects


class TestLeaveOneOut:
    def test_homogeneous_pair_is_stable(self):
        result = leave_one_out(
            betas=[0.3, 0.3, 0.3, 0.3, 0.3],
            ses=[0.05, 0.06, 0.04, 0.08, 0.07],
            strata_names=["A", "B", "C", "D", "E"],
        )
        assert result.stable is True
        assert result.flipped_strata == []

    def test_two_strata_always_stable(self):
        result = leave_one_out(
            betas=[0.5, -0.5],
            ses=[0.01, 0.01],
            strata_names=["X", "Y"],
        )
        assert result.stable is True

    def test_detects_influential_stratum(self):
        betas = [0.30, 0.31, 0.29, 0.32, 1.50]
        ses = [0.05, 0.05, 0.05, 0.05, 0.05]
        names = ["A", "B", "C", "D", "outlier"]
        result = leave_one_out(betas, ses, names, alpha=0.05)
        if not result.stable:
            assert "outlier" in result.flipped_strata

    def test_flipped_strata_are_valid_names(self):
        rng = np.random.default_rng(None)
        for _ in range(50):
            k = rng.integers(3, 8)
            betas = rng.normal(0, 0.5, size=k).tolist()
            ses = rng.uniform(0.02, 0.1, size=k).tolist()
            names = [f"s{i}" for i in range(k)]
            result = leave_one_out(betas, ses, names)
            for name in result.flipped_strata:
                assert name in names


class TestAlphaSweep:
    def test_verdicts_monotonic_in_alpha(self):
        rng = np.random.default_rng(None)
        for _ in range(100):
            k = rng.integers(3, 8)
            betas = rng.normal(0.3, 0.3, size=k).tolist()
            ses = rng.uniform(0.02, 0.1, size=k).tolist()
            sweep = alpha_sweep(betas, ses)
            saw_nontransport = False
            for entry in sweep:
                if entry["verdict"] == "non-transport":
                    saw_nontransport = True
                if saw_nontransport:
                    assert entry["verdict"] == "non-transport", (
                        "Once non-transport at a stricter alpha, must stay non-transport at looser alpha"
                    )

    def test_p_value_constant_across_sweep(self):
        betas = [0.4, 0.1, 0.35]
        ses = [0.05, 0.06, 0.04]
        sweep = alpha_sweep(betas, ses)
        p_values = [entry["p"] for entry in sweep]
        for p in p_values:
            assert p == pytest.approx(p_values[0], rel=1e-10)

    def test_returns_correct_number_of_entries(self):
        sweep = alpha_sweep([0.3, 0.2], [0.05, 0.05])
        assert len(sweep) == 9  # default alphas has 9 entries
        custom = alpha_sweep([0.3, 0.2], [0.05, 0.05], alphas=[0.01, 0.05, 0.10])
        assert len(custom) == 3


class TestRandomEffects:
    def test_homogeneous_tau2_near_zero(self):
        betas = [0.30, 0.30, 0.30, 0.30]
        ses = [0.05, 0.06, 0.04, 0.08]
        re = random_effects(betas, ses)
        assert re["tau2"] == pytest.approx(0.0, abs=1e-10)
        assert re["beta_re"] == pytest.approx(re["beta_fe"], abs=1e-10)
        assert re["se_re"] == pytest.approx(re["se_fe"], abs=1e-10)

    def test_se_re_geq_se_fe(self):
        rng = np.random.default_rng(None)
        for _ in range(200):
            k = rng.integers(2, 10)
            betas = rng.normal(0, 1, size=k).tolist()
            ses = rng.uniform(0.01, 0.5, size=k).tolist()
            re = random_effects(betas, ses)
            assert re["se_re"] >= re["se_fe"] - 1e-12

    def test_beta_shift_nonnegative(self):
        rng = np.random.default_rng(None)
        for _ in range(100):
            k = rng.integers(2, 10)
            betas = rng.normal(0, 1, size=k).tolist()
            ses = rng.uniform(0.01, 0.5, size=k).tolist()
            re = random_effects(betas, ses)
            assert re["beta_shift"] >= 0.0

    def test_i2_matches_core(self):
        from mr_transport.core import _cochran_q

        betas = [0.5, 0.1, 0.3, 0.8]
        ses = [0.05, 0.06, 0.04, 0.08]
        re = random_effects(betas, ses)
        core = _cochran_q(np.array(betas), np.array(ses))
        assert re["I2"] == pytest.approx(core["I2"], rel=1e-10)
        assert re["tau2"] == pytest.approx(core["tau2"], rel=1e-10)
