"""Modal wrapper for vector Q power simulation.

Distributes the parameter grid across multiple containers for parallel execution.
Each container runs a chunk of the grid; results are merged and saved to a Volume.

Usage:
    modal run experiments/batch6_vector_extension/scripts/modal_power_simulation.py --detach
"""

import modal

app = modal.App("vector-q-power-simulation-sheaf-transportability")

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install(
        "numpy==2.2.6",
        "scipy==1.15.3",
        "tqdm==4.67.1",
        "matplotlib==3.10.3",
    )
)

vol = modal.Volume.from_name("vector-q-power-sim", create_if_missing=True)

RESULTS_DIR = "/data/results"
N_SIMS_POWER = 2000
N_SIMS_NULL = 10000
N_CHUNKS = 12


FULL_GRID = {
    "theta": [0, 5, 10, 15, 20, 30, 45, 60, 75, 90],
    "rho": [0.0, 0.3, 0.6, 0.9],
    "K": [4, 6, 8],
    "d": [5, 15, 25],
}


def build_grid(grid_spec):
    cells = []
    for theta in grid_spec["theta"]:
        for rho in grid_spec["rho"]:
            for K in grid_spec["K"]:
                for d in grid_spec["d"]:
                    cells.append({"theta": theta, "rho": rho, "K": K, "d": d})
    return cells


@app.function(
    image=image,
    timeout=86400,
    memory=4096,
    cpu=2.0,
)
def run_power_chunk(chunk_cells, chunk_id, n_sims):
    import json
    import numpy as np
    from datetime import datetime
    from scipy import stats
    from tqdm import tqdm

    print(f"[{datetime.now().isoformat()}] Chunk {chunk_id}: {len(chunk_cells)} cells x {n_sims} sims")

    def simulate_one(K, d, theta_deg, rho, se_scale=0.06, alpha=0.05):
        beta_0 = np.zeros(d)
        beta_0[0] = 0.2
        if d > 1:
            beta_0[1] = 0.1

        theta_rad = np.radians(theta_deg)
        cos_t, sin_t = np.cos(theta_rad), np.sin(theta_rad)

        betas_true = np.zeros((K, d))
        betas_true[0] = beta_0
        for k in range(1, K):
            b = beta_0.copy()
            b[0] = cos_t * beta_0[0] - sin_t * beta_0[1]
            b[1] = sin_t * beta_0[0] + cos_t * beta_0[1]
            betas_true[k] = b

        se_matrix = np.full((K, d), se_scale)
        rho_mat = (1 - rho) * np.eye(d) + rho * np.ones((d, d))

        beta_obs = np.zeros((K, d))
        cov_matrices = np.zeros((K, d, d))
        for k in range(K):
            cov_k = np.diag(se_matrix[k]) @ rho_mat @ np.diag(se_matrix[k])
            cov_matrices[k] = cov_k
            beta_obs[k] = np.random.multivariate_normal(betas_true[k], cov_k)

        W = np.array([np.linalg.inv(cov_matrices[k]) for k in range(K)])
        W_sum = np.sum(W, axis=0)
        W_sum_inv = np.linalg.inv(W_sum)
        beta_bar = W_sum_inv @ np.sum([W[k] @ beta_obs[k] for k in range(K)], axis=0)

        Q_V = 0.0
        for k in range(K):
            diff = beta_obs[k] - beta_bar
            Q_V += diff @ W[k] @ diff

        df_vec = d * (K - 1)
        p_vec = 1.0 - stats.chi2.cdf(Q_V, df_vec)
        vector_reject = p_vec < alpha

        alpha_bonf = alpha / d
        n_scalar_reject = 0
        for j in range(d):
            w_j = 1.0 / se_matrix[:, j] ** 2
            beta_bar_j = np.sum(w_j * beta_obs[:, j]) / np.sum(w_j)
            Q_j = np.sum(w_j * (beta_obs[:, j] - beta_bar_j) ** 2)
            p_j = 1.0 - stats.chi2.cdf(Q_j, K - 1)
            if p_j < alpha_bonf:
                n_scalar_reject += 1

        return bool(vector_reject), n_scalar_reject > 0

    results = []
    for cell in tqdm(chunk_cells, desc=f"Chunk {chunk_id}"):
        theta, rho_val, K, d = cell["theta"], cell["rho"], cell["K"], cell["d"]
        vec_rej = 0
        sca_rej = 0
        for _ in range(n_sims):
            vr, sr = simulate_one(K, d, theta, rho_val)
            vec_rej += vr
            sca_rej += sr

        results.append({
            "theta": theta, "rho": rho_val, "K": K, "d": d,
            "n_sims": n_sims,
            "vector_power": vec_rej / n_sims,
            "scalar_power": sca_rej / n_sims,
        })

    print(f"[{datetime.now().isoformat()}] Chunk {chunk_id} done: {len(results)} cells")
    return results


@app.function(
    image=image,
    timeout=86400,
    memory=4096,
    cpu=2.0,
)
def run_null_calibration_cell(K, d, n_sims, alpha=0.05):
    import numpy as np
    from datetime import datetime
    from scipy import stats
    from tqdm import tqdm

    print(f"[{datetime.now().isoformat()}] Null calibration: K={K}, d={d}, n={n_sims}")

    Q_values = []
    vec_rejects = 0
    scalar_rejects = 0

    for _ in tqdm(range(n_sims), desc=f"Null K={K} d={d}"):
        se_matrix = np.full((K, d), 0.06)
        beta_obs = np.random.normal(0.2, 0.06, size=(K, d))

        cov_matrices = np.array([np.diag(se_matrix[k] ** 2) for k in range(K)])
        W = np.array([np.linalg.inv(cov_matrices[k]) for k in range(K)])
        W_sum = np.sum(W, axis=0)
        W_sum_inv = np.linalg.inv(W_sum)
        beta_bar = W_sum_inv @ np.sum([W[k] @ beta_obs[k] for k in range(K)], axis=0)

        Q_V = 0.0
        for k in range(K):
            diff = beta_obs[k] - beta_bar
            Q_V += diff @ W[k] @ diff

        Q_values.append(Q_V)
        df_vec = d * (K - 1)
        p_vec = 1.0 - stats.chi2.cdf(Q_V, df_vec)
        if p_vec < alpha:
            vec_rejects += 1

        alpha_bonf = alpha / d
        any_rej = False
        for j in range(d):
            w_j = 1.0 / se_matrix[:, j] ** 2
            beta_bar_j = np.sum(w_j * beta_obs[:, j]) / np.sum(w_j)
            Q_j = np.sum(w_j * (beta_obs[:, j] - beta_bar_j) ** 2)
            p_j = 1.0 - stats.chi2.cdf(Q_j, K - 1)
            if p_j < alpha_bonf:
                any_rej = True
                break
        if any_rej:
            scalar_rejects += 1

    Q_arr = np.sort(Q_values)
    df_vec = d * (K - 1)
    pctiles = np.linspace(1, 99, 50)
    theoretical = stats.chi2.ppf(pctiles / 100, df_vec).tolist()
    empirical = np.percentile(Q_arr, pctiles).tolist()

    print(f"[{datetime.now().isoformat()}] Null K={K} d={d}: "
          f"type1_vec={vec_rejects/n_sims:.3f}, type1_sca={scalar_rejects/n_sims:.3f}")

    return {
        "K": K, "d": d, "df": df_vec,
        "n_sims": n_sims,
        "empirical_type1_vector": vec_rejects / n_sims,
        "empirical_type1_scalar": scalar_rejects / n_sims,
        "nominal_alpha": alpha,
        "qq_theoretical": theoretical,
        "qq_empirical": empirical,
    }


@app.function(
    image=image,
    volumes={"/data": vol},
    timeout=86400,
    memory=4096,
    cpu=2.0,
)
def merge_and_save(power_results_nested, null_results, grid_spec, n_sims):
    import json
    from datetime import datetime
    from pathlib import Path

    power_results = []
    for chunk in power_results_nested:
        power_results.extend(chunk)

    results_dir = Path(RESULTS_DIR)
    results_dir.mkdir(parents=True, exist_ok=True)

    output = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "grid": grid_spec,
            "n_sims_power": n_sims,
            "n_sims_null": N_SIMS_NULL,
            "n_cells": len(power_results),
            "mode": "modal_distributed",
        },
        "power_results": power_results,
        "null_calibration": null_results,
    }

    output_path = results_dir / "power_simulation_results.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"[{datetime.now().isoformat()}] Saved to {output_path}")
    print(f"  Power cells: {len(power_results)}")
    print(f"  Null cells: {len(null_results)}")

    print("\n" + "=" * 60)
    print("NULL CALIBRATION SUMMARY")
    print("=" * 60)
    for r in null_results:
        status = "OK" if abs(r["empirical_type1_vector"] - 0.05) < 0.015 else "CHECK"
        print(f"  K={r['K']:2d}, d={r['d']:2d} (df={r['df']:3d}): "
              f"vector={r['empirical_type1_vector']:.3f}, "
              f"scalar={r['empirical_type1_scalar']:.3f}  [{status}]")

    print("\n" + "=" * 60)
    print("POWER HIGHLIGHTS")
    print("=" * 60)
    for r in sorted(power_results, key=lambda x: (x["d"], x["K"], x["rho"], x["theta"])):
        if r["theta"] in [0, 30, 60, 90] and r["rho"] in [0.0, 0.6]:
            print(f"  theta={r['theta']:3d}, rho={r['rho']:.1f}, K={r['K']}, d={r['d']:2d}: "
                  f"vec={r['vector_power']:.3f}, sca={r['scalar_power']:.3f}")

    return str(output_path)


@app.local_entrypoint()
def main():
    from datetime import datetime
    import math

    print(f"[{datetime.now().isoformat()}] Launching vector Q power simulation on Modal")
    print(f"Grid: {FULL_GRID}")
    print(f"N_SIMS_POWER={N_SIMS_POWER}, N_SIMS_NULL={N_SIMS_NULL}, N_CHUNKS={N_CHUNKS}")

    cells = build_grid(FULL_GRID)
    print(f"Total grid cells: {len(cells)}")
    print(f"Total simulations: {len(cells) * N_SIMS_POWER + len(FULL_GRID['K']) * len(FULL_GRID['d']) * N_SIMS_NULL:,}")

    chunk_size = math.ceil(len(cells) / N_CHUNKS)
    chunks = [cells[i:i + chunk_size] for i in range(0, len(cells), chunk_size)]
    print(f"Distributing across {len(chunks)} chunks of ~{chunk_size} cells each")

    print(f"\n[{datetime.now().isoformat()}] Launching power simulation chunks...")
    power_futures = []
    for i, chunk in enumerate(chunks):
        power_futures.append(run_power_chunk.spawn(chunk, i, N_SIMS_POWER))

    print(f"[{datetime.now().isoformat()}] Launching null calibration cells...")
    null_futures = []
    for K in FULL_GRID["K"]:
        for d in FULL_GRID["d"]:
            null_futures.append(run_null_calibration_cell.spawn(K, d, N_SIMS_NULL))

    print(f"[{datetime.now().isoformat()}] Waiting for {len(power_futures)} power chunks + {len(null_futures)} null cells...")

    power_results = [f.get() for f in power_futures]
    null_results = [f.get() for f in null_futures]

    print(f"\n[{datetime.now().isoformat()}] All done. Merging results...")
    output_path = merge_and_save.remote(power_results, null_results, FULL_GRID, N_SIMS_POWER)
    print(f"Results saved to Modal volume at {output_path}")
    print(f"Download with: modal volume get vector-q-power-sim {output_path}")
