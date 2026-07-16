import numpy as np
import pytest

from mr_transport.core import test_transport as run_transport
from mr_transport.simulate import simulate_catalog, simulate_pair


class TestSimulatePair:
    def test_tau_zero_gives_transport(self):
        for _ in range(50):
            pair = simulate_pair(k=5, tau=0.0)
            assert pair["ground_truth"] == "transport"

    def test_tau_positive_gives_nontransport(self):
        for _ in range(50):
            pair = simulate_pair(k=5, tau=0.3)
            assert pair["ground_truth"] == "non-transport"

    def test_correct_number_of_strata(self):
        for k in [2, 5, 10, 20]:
            pair = simulate_pair(k=k)
            assert len(pair["strata"]) == k

    def test_all_ses_positive_and_finite(self):
        for _ in range(100):
            pair = simulate_pair(k=6, tau=0.2)
            for s in pair["strata"]:
                assert np.isfinite(s["beta"])
                assert np.isfinite(s["se"])
                assert s["se"] > 0

    def test_strata_have_names(self):
        pair = simulate_pair(k=3, strata_prefix="ancestry")
        names = [s["name"] for s in pair["strata"]]
        assert names == ["ancestry_1", "ancestry_2", "ancestry_3"]

    def test_params_recorded(self):
        pair = simulate_pair(k=4, beta_true=0.5, tau=0.1)
        assert pair["params"]["k"] == 4
        assert pair["params"]["beta_true"] == pytest.approx(0.5)
        assert pair["params"]["tau"] == pytest.approx(0.1)


class TestSimulateCatalog:
    def test_correct_count(self):
        cat = simulate_catalog(n_transport=15, n_nontransport=8, seed=1)
        assert len(cat) == 23
        assert sum(1 for p in cat if p["ground_truth"] == "transport") == 15
        assert sum(1 for p in cat if p["ground_truth"] == "non-transport") == 8

    def test_all_pairs_have_ids(self):
        cat = simulate_catalog(n_transport=5, n_nontransport=5, seed=2)
        ids = [p["id"] for p in cat]
        assert len(set(ids)) == len(ids)

    def test_classification_accuracy_above_chance(self):
        n_transport, n_nontransport = 300, 200
        cat = simulate_catalog(
            n_transport=n_transport,
            n_nontransport=n_nontransport,
            seed=7,
        )
        correct = 0
        for pair in cat:
            r = run_transport(
                betas=[s["beta"] for s in pair["strata"]],
                ses=[s["se"] for s in pair["strata"]],
            )
            if r.verdict == pair["ground_truth"]:
                correct += 1
        accuracy = correct / len(cat)
        assert accuracy > 0.70, f"Expected >70% accuracy, got {accuracy:.1%}"
