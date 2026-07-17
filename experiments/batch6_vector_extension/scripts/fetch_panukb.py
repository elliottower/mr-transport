"""Fetch per-ancestry GWAS summary statistics from Pan-UKB for blood traits.

Uses tabix to query remote bgzipped+indexed TSVs on S3 — only downloads
the specific rows we need, not the full 100MB-1GB flat files.

Usage:
    uv run python experiments/batch6_vector_extension/scripts/fetch_panukb.py
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
from tqdm import tqdm

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data"

ANCESTRIES = ["AFR", "AMR", "CSA", "EAS", "EUR", "MID"]

PANUKB_DATA = "https://pan-ukb-us-east-1.s3.amazonaws.com/sumstats_flat_files"
PANUKB_IDX = "https://pan-ukb-us-east-1.s3.amazonaws.com/sumstats_flat_files_tabix"

COLUMNS = [
    "chr", "pos", "ref", "alt",
    "af_meta_hq", "beta_meta_hq", "se_meta_hq",
    "neglog10_pval_meta_hq", "neglog10_pval_heterogeneity_hq",
    "af_meta", "beta_meta", "se_meta",
    "neglog10_pval_meta", "neglog10_pval_heterogeneity",
    "af_AFR", "af_AMR", "af_CSA", "af_EAS", "af_EUR", "af_MID",
    "beta_AFR", "beta_AMR", "beta_CSA", "beta_EAS", "beta_EUR", "beta_MID",
    "se_AFR", "se_AMR", "se_CSA", "se_EAS", "se_EUR", "se_MID",
    "neglog10_pval_AFR", "neglog10_pval_AMR", "neglog10_pval_CSA",
    "neglog10_pval_EAS", "neglog10_pval_EUR", "neglog10_pval_MID",
    "low_confidence_AFR", "low_confidence_AMR", "low_confidence_CSA",
    "low_confidence_EAS", "low_confidence_EUR", "low_confidence_MID",
]

BLOOD_TRAITS = [
    ("30000", "White blood cell count"),
    ("30010", "Red blood cell count"),
    ("30020", "Haemoglobin concentration"),
    ("30030", "Haematocrit"),
    ("30040", "Mean corpuscular volume"),
    ("30050", "Mean corpuscular haemoglobin"),
    ("30060", "Mean corpuscular haemoglobin concentration"),
    ("30070", "Red blood cell distribution width"),
    ("30080", "Platelet count"),
    ("30090", "Platelet distribution width"),
    ("30100", "Mean platelet volume"),
    ("30110", "Platelet crit"),
    ("30120", "Lymphocyte count"),
    ("30130", "Monocyte count"),
    ("30140", "Neutrophil count"),
    ("30150", "Eosinophil count"),
    ("30180", "Lymphocyte percentage"),
    ("30190", "Monocyte percentage"),
    ("30200", "Neutrophil percentage"),
    ("30210", "Eosinophil percentage"),
    ("30220", "Basophil percentage"),
    ("30240", "Reticulocyte percentage"),
    ("30250", "Reticulocyte count"),
    ("30260", "Mean reticulocyte volume"),
    ("30270", "Mean sphered cell volume"),
    ("30280", "Immature reticulocyte fraction"),
    ("30290", "High light scatter reticulocyte percentage"),
]

TARGET_LOCI = [
    ("rs2814778", "1", 159174683, "ACKR1", "Duffy antigen — positive control for rotation"),
    ("rs1354034", "3", 56849749, "ARHGEF3", "Platelet count pleiotropic"),
    ("rs3184504", "12", 111884608, "SH2B3", "Multi-blood-trait pleiotropic"),
    ("rs12722489", "10", 6130949, "IL2RA", "Immune/blood pleiotropic"),
    ("rs2476601", "1", 114377568, "PTPN22", "Autoimmune/blood pleiotropic"),
    ("rs855791", "22", 37462936, "TMPRSS6", "Iron metabolism/blood"),
    ("rs9349379", "6", 12903957, "PHACTR1", "CAD + blood pressure"),
    ("rs11065987", "12", 112059557, "BRAP", "Blood trait pleiotropic"),
    ("rs6795744", "3", 150289833, "IRGM", "Neutrophil/monocyte"),
]


def panukb_url(pheno_code):
    """Build combined data+index URL using htslib ##idx## syntax."""
    data = f"{PANUKB_DATA}/continuous-{pheno_code}-both_sexes-irnt.tsv.bgz"
    idx = f"{PANUKB_IDX}/continuous-{pheno_code}-both_sexes-irnt.tsv.bgz.tbi"
    return f"{data}##idx##{idx}"


def tabix_query(url, chrom, pos):
    """Query a single position from a remote bgzipped+indexed TSV."""
    region = f"{chrom}:{pos}-{pos}"
    result = subprocess.run(
        ["tabix", url, region],
        capture_output=True, text=True, timeout=60,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return None
    for line in result.stdout.strip().split("\n"):
        fields = line.split("\t")
        if len(fields) >= len(COLUMNS) and int(fields[1]) == pos:
            return dict(zip(COLUMNS, fields))
    return None


def parse_ancestry_data(row):
    """Extract per-ancestry beta, se, af, p, low_confidence from a parsed row."""
    out = {}
    for anc in ANCESTRIES:
        try:
            beta = float(row[f"beta_{anc}"])
            se = float(row[f"se_{anc}"])
            af = float(row[f"af_{anc}"])
            nlp = float(row[f"neglog10_pval_{anc}"])
            lc = row[f"low_confidence_{anc}"].lower() == "true"
        except (ValueError, KeyError):
            continue
        if np.isnan(beta) or np.isnan(se) or se <= 0:
            continue
        out[anc] = {
            "beta": beta, "se": se, "af": af,
            "neglog10_pval": nlp, "low_confidence": lc,
        }
    return out


def fetch_all(traits, loci):
    """Fetch all trait x locus combinations via tabix."""
    data = {}
    total = len(traits) * len(loci)
    pbar = tqdm(total=total, desc="Fetching Pan-UKB data")
    for rsid, chrom, pos, gene, desc in loci:
        locus_traits = {}
        for pheno_code, pheno_name in traits:
            pbar.update(1)
            pbar.set_postfix_str(f"{gene}/{pheno_name[:20]}")
            url = panukb_url(pheno_code)
            try:
                row = tabix_query(url, chrom, pos)
            except subprocess.TimeoutExpired:
                print(f"\n  TIMEOUT: {gene}/{pheno_code}")
                continue
            if row is None:
                continue
            anc_data = parse_ancestry_data(row)
            if anc_data:
                locus_traits[pheno_code] = {
                    "name": pheno_name,
                    "ref": row["ref"],
                    "alt": row["alt"],
                    "beta_meta": float(row.get("beta_meta", "nan")),
                    "se_meta": float(row.get("se_meta", "nan")),
                    "ancestries": anc_data,
                }
        if locus_traits:
            data[rsid] = {
                "gene": gene, "chr": chrom, "pos": pos,
                "description": desc, "traits": locus_traits,
            }
    pbar.close()
    return data


def build_analysis_json(raw_data, traits):
    """Build the JSON format expected by run_vector_analysis.py.

    For each locus, creates a (K, d) matrix of betas and SEs where
    K = number of ancestries with data across all selected traits,
    d = number of traits.
    """
    trait_codes = [t[0] for t in traits]
    trait_names = {t[0]: t[1] for t in traits}

    output = {
        "loci": {},
        "phenotypic_correlations": {},
        "metadata": {
            "source": "Pan-UKB v2 (tabix remote query)",
            "date": datetime.now().isoformat(),
            "n_loci": 0,
            "n_traits": 0,
            "n_ancestries": 0,
        },
    }

    for rsid, locus in raw_data.items():
        available_traits = [c for c in trait_codes if c in locus["traits"]]
        if len(available_traits) < 2:
            print(f"  {rsid} ({locus['gene']}): <2 traits, skipping")
            continue

        all_ancestries = set()
        for tc in available_traits:
            all_ancestries.update(locus["traits"][tc]["ancestries"].keys())

        good_ancestries = []
        for anc in sorted(all_ancestries):
            n_traits_with_anc = sum(
                1 for tc in available_traits
                if anc in locus["traits"][tc]["ancestries"]
            )
            if n_traits_with_anc == len(available_traits):
                good_ancestries.append(anc)

        if len(good_ancestries) < 3:
            second_pass = []
            for anc in sorted(all_ancestries):
                n = sum(
                    1 for tc in available_traits
                    if anc in locus["traits"][tc]["ancestries"]
                )
                if n >= len(available_traits) * 0.8:
                    second_pass.append(anc)
            if len(second_pass) >= 3:
                good_ancestries = second_pass
                available_traits = [
                    tc for tc in available_traits
                    if all(a in locus["traits"][tc]["ancestries"] for a in good_ancestries)
                ]

        if len(good_ancestries) < 3:
            print(f"  {rsid} ({locus['gene']}): <3 shared ancestries "
                  f"({len(good_ancestries)}), skipping")
            continue

        betas = []
        ses = []
        low_conf = []
        for anc in good_ancestries:
            b_row, s_row, lc_row = [], [], []
            for tc in available_traits:
                d = locus["traits"][tc]["ancestries"][anc]
                b_row.append(d["beta"])
                s_row.append(d["se"])
                lc_row.append(d["low_confidence"])
            betas.append(b_row)
            ses.append(s_row)
            low_conf.append(lc_row)

        output["loci"][rsid] = {
            "gene": locus["gene"],
            "chr": locus["chr"],
            "pos": locus["pos"],
            "description": locus["description"],
            "ancestries": good_ancestries,
            "traits": [trait_names.get(tc, tc) for tc in available_traits],
            "trait_codes": available_traits,
            "betas": betas,
            "ses": ses,
            "low_confidence": low_conf,
        }
        output["metadata"]["n_loci"] += 1

    if output["loci"]:
        all_n_traits = [len(v["traits"]) for v in output["loci"].values()]
        all_n_anc = [len(v["ancestries"]) for v in output["loci"].values()]
        output["metadata"]["n_traits"] = max(all_n_traits)
        output["metadata"]["n_ancestries"] = max(all_n_anc)

    return output


def build_phenotypic_correlations(trait_names):
    """Build approximate phenotypic correlation matrix for blood traits.

    Based on UK Biobank estimates (Vuckovic et al. 2020 Cell,
    Astle et al. 2016 Cell).
    """
    known = {
        ("White blood cell count", "Neutrophil count"): 0.93,
        ("White blood cell count", "Lymphocyte count"): 0.72,
        ("White blood cell count", "Monocyte count"): 0.50,
        ("White blood cell count", "Eosinophil count"): 0.30,
        ("White blood cell count", "Basophil count"): 0.20,
        ("Neutrophil count", "Monocyte count"): 0.35,
        ("Neutrophil count", "Lymphocyte count"): 0.15,
        ("Neutrophil count", "Eosinophil count"): 0.10,
        ("Neutrophil count", "Basophil count"): 0.12,
        ("Lymphocyte count", "Monocyte count"): 0.18,
        ("Lymphocyte count", "Eosinophil count"): 0.15,
        ("Monocyte count", "Eosinophil count"): 0.12,
        ("Red blood cell count", "Haemoglobin concentration"): 0.70,
        ("Red blood cell count", "Haematocrit"): 0.85,
        ("Haemoglobin concentration", "Haematocrit"): 0.95,
        ("Mean corpuscular volume", "Mean corpuscular haemoglobin"): 0.90,
        ("Mean corpuscular volume", "Mean corpuscular haemoglobin concentration"): 0.40,
        ("Mean corpuscular haemoglobin", "Mean corpuscular haemoglobin concentration"): 0.65,
        ("Red blood cell count", "Mean corpuscular volume"): -0.50,
        ("Platelet count", "Platelet crit"): 0.95,
        ("Platelet count", "Mean platelet volume"): -0.35,
        ("Platelet count", "Platelet distribution width"): -0.30,
        ("Mean platelet volume", "Platelet distribution width"): 0.85,
        ("Red blood cell count", "Red blood cell distribution width"): -0.30,
    }

    d = len(trait_names)
    rho = np.eye(d)
    for i, t1 in enumerate(trait_names):
        for j, t2 in enumerate(trait_names):
            if i == j:
                continue
            for key in [(t1, t2), (t2, t1)]:
                if key in known:
                    rho[i, j] = known[key]
                    break

    eigvals, eigvecs = np.linalg.eigh(rho)
    eigvals = np.maximum(eigvals, 0.01)
    rho_psd = eigvecs @ np.diag(eigvals) @ eigvecs.T
    d_inv = np.diag(1.0 / np.sqrt(np.diag(rho_psd)))
    rho_psd = d_inv @ rho_psd @ d_inv
    return rho_psd.tolist()


def main():
    print("Pan-UKB Blood Trait Data Acquisition (tabix remote)")
    print("=" * 55)
    print(f"Target: {len(TARGET_LOCI)} loci x {len(BLOOD_TRAITS)} traits x {len(ANCESTRIES)} ancestries")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()

    DATA_DIR.mkdir(exist_ok=True)

    try:
        subprocess.run(["tabix", "--version"], capture_output=True, timeout=5, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("ERROR: tabix not found. Install with: brew install htslib")
        sys.exit(1)

    print("Querying Pan-UKB S3 via tabix (no full download needed)...")
    print()
    raw = fetch_all(BLOOD_TRAITS, TARGET_LOCI)

    raw_path = DATA_DIR / "panukb_raw.json"
    with open(raw_path, "w") as f:
        json.dump(raw, f, indent=2, default=str)
    print(f"\nRaw data saved to {raw_path}")

    print("\nBuilding analysis matrices...")
    output = build_analysis_json(raw, BLOOD_TRAITS)

    # Add phenotypic correlations for the largest trait set
    if output["loci"]:
        largest_locus = max(output["loci"].values(), key=lambda v: len(v["traits"]))
        rho = build_phenotypic_correlations(largest_locus["traits"])
        output["phenotypic_correlations"] = {"EUR": rho}

    output_path = DATA_DIR / "panukb_locus_data.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Analysis data saved to {output_path}")

    print(f"\nSummary: {output['metadata']['n_loci']} loci ready for analysis")
    for rsid, locus in output["loci"].items():
        K = len(locus["ancestries"])
        d = len(locus["traits"])
        n_lc = sum(sum(row) for row in locus["low_confidence"])
        print(f"  {rsid} ({locus['gene']}): K={K} ancestries, d={d} traits"
              f"{f', {n_lc} low-confidence cells' if n_lc > 0 else ''}")


if __name__ == "__main__":
    main()
