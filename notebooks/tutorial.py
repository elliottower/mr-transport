"""Tutorial: Using mr-transport to classify MR transportability.

This script demonstrates the mr-transport library on three cases:
1. A clear non-transportable pair from the catalog (HLA-DRB1 → RA)
2. An underpowered pair where the test honestly abstains (SBP → AD)
3. Synthetic data with known ground truth
4. Bring-your-own-data: plug in your own betas and SEs

Run as: python notebooks/tutorial.py
"""

import mr_transport as mrt
from mr_transport.sensitivity import leave_one_out, alpha_sweep

# %% Case 1: Clear non-transport — HLA-DRB1 shared epitope → RA risk
# EUR OR~5.0, EAS OR~3.3, AFR OR~2.2. Dramatic cross-ancestry variation
# in allele architecture makes this a textbook non-transportable pair.

result = mrt.test_transport(
    betas=[1.6, 1.2, 0.8, 1.0],
    ses=[0.04, 0.07, 0.12, 0.10],
    strata_names=["EUR", "EAS", "AFR", "HISP"],
)
print("=== Case 1: HLA-DRB1 → RA (expected: non-transport) ===")
print(result)
print(f"  Underpowered? {result.underpowered}")
print()


# %% Case 2: Underpowered — SBP → Alzheimer's disease
# I²=58% says heterogeneity exists, but only 4 strata → power=0.38.
# The test correctly reports "transport" (non-significant) but the low
# power and high I² mean this is honest uncertainty, not evidence of
# homogeneity. The right conclusion: get more ancestry strata.

result_sbp = mrt.test_transport(
    betas=[0.10, -0.05, 0.15, 0.02],
    ses=[0.04, 0.05, 0.08, 0.10],
    strata_names=["EUR_midlife", "EUR_latelife", "EAS", "AFR"],
)
print("=== Case 2: SBP → AD (expected: non-transport, but underpowered) ===")
print(result_sbp)
print(f"  Underpowered? {result_sbp.underpowered}")

k_needed = mrt.strata_needed(I2=result_sbp.I2, target_power=0.80)
print(f"  Strata needed for 80% power at this I²: {k_needed}")
print()


# %% Case 3: Synthetic data with known ground truth
# Generate 20 transportable + 10 non-transportable pairs, classify all,
# and check accuracy against the planted labels.

catalog = mrt.simulate_catalog(n_transport=20, n_nontransport=10, seed=42)
correct = 0
for pair in catalog:
    r = mrt.test_transport(
        betas=[s["beta"] for s in pair["strata"]],
        ses=[s["se"] for s in pair["strata"]],
        strata_names=[s["name"] for s in pair["strata"]],
    )
    if r.verdict == pair["ground_truth"]:
        correct += 1

print(f"=== Case 3: Synthetic catalog (30 pairs, known ground truth) ===")
print(f"  Accuracy: {correct}/{len(catalog)} ({100*correct/len(catalog):.0f}%)")
print()


# %% Case 4: Bring your own data
# Replace these with your own per-stratum MR estimates.

print("=== Case 4: Bring your own data ===")
my_result = mrt.test_transport(
    betas=[0.25, 0.23, 0.28],        # your per-stratum betas
    ses=[0.05, 0.06, 0.07],           # your per-stratum SEs
    strata_names=["EUR", "EAS", "AFR"],
)
print(my_result)

# Sensitivity: how stable is this across alpha choices?
sweep = alpha_sweep(
    betas=[0.25, 0.23, 0.28],
    ses=[0.05, 0.06, 0.07],
)
print("  Alpha sweep:")
for s in sweep:
    print(f"    α={s['alpha']:.3f}: {s['verdict']:15s} (power={s['power']:.2f})")

# LOO: does the verdict depend on a single stratum?
loo = leave_one_out(
    betas=[0.25, 0.23, 0.28],
    ses=[0.05, 0.06, 0.07],
    strata_names=["EUR", "EAS", "AFR"],
)
print(f"  LOO stable: {loo.stable}")
if not loo.stable:
    print(f"  Flips when dropping: {loo.flipped_strata}")
print()


# %% Load the real 71-pair catalog
real_catalog = mrt.load_catalog()
print(f"=== Bundled catalog: {len(real_catalog)} pairs ===")
domains = {}
for p in real_catalog:
    d = p["domain"]
    domains[d] = domains.get(d, 0) + 1
for d, n in sorted(domains.items()):
    print(f"  {d}: {n} pairs")
