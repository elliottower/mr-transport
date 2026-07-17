"""
Swap hand-entered approximate strata with real published per-ancestry MR estimates.

Sources:
  - Wang 2022 Genome Medicine (PMC9195360): LDL/HDL/TG/SBP/T2D/BMI → CAD
  - Circulation 2025 (PMC12165552): Lp(a) → MI
  - O'Loughlin 2023 BMC Medicine (PMC9893684): BMI → depression
  - Tyrrell 2019 Int J Epidemiol 48(3):834-848: BMI → depression EUR
  - Kember 2024 Alcohol Clin Exp Res (DOI: 10.1111/acer.15445): Alcohol → CHD, 3 ancestries
  - Wootton 2020 Psychol Med (PMC7610182): Smoking initiation → SCZ EUR
  - Su 2022 Schizophrenia (PMC9463183): Smoking initiation → SCZ EAS
  - Ooi 2019 Int J Epidemiol (PMC6659372): BMI → breast cancer EUR (BCAC)
  - Wu 2025 Medicine Baltimore (PMID 40587687): BMI → breast cancer EAS (PheWAS)
  - Hemani 2025 CAMeRa (doi:10.21203/rs.3.rs-6091701/v1): BMI → T2D, EUR vs EAS
  - Wang 2022 IL6R MVP (medrxiv 2022.09.24.22280325): IL6R → IHD, EUR vs AFR
  - Hemani 2025 CAMeRa analysis repo (github.com/yoonsucho/camera_analysis): LDL → stroke, 5 ancestries

Conversion: beta = ln(OR), SE = (ln(CI_upper) - ln(CI_lower)) / (2 * 1.96)
For CAMeRa pairs: logOR per SD (BMI→T2D from paper text, LDL→stroke from analysis repo HTML).
"""

import json
import math
import copy
from pathlib import Path

DATA_DIR = Path(__file__).parent

def or_to_beta_se(or_val, ci_lower, ci_upper):
    beta = math.log(or_val)
    se = (math.log(ci_upper) - math.log(ci_lower)) / (2 * 1.96)
    return round(beta, 4), round(se, 4)


REPLACEMENTS = {
    "LDL_CAD_MR": {
        "source_papers": ["Wang 2022 Genome Medicine (PMC9195360)"],
        "strata": [
            {"name": "EUR_UKBB", "beta": 0.5988, "se": 0.0629,
             "source": "Wang 2022, UK Biobank MR-IVW, OR=1.82 (1.61-2.06)"},
            {"name": "EAS_BBJ", "beta": 0.5710, "se": 0.0846,
             "source": "Wang 2022, Biobank Japan MR-IVW, OR=1.77 (1.50-2.09)"},
        ]
    },
    "HDL_CAD_MR": {
        "source_papers": ["Wang 2022 Genome Medicine (PMC9195360)"],
        "strata": [
            {"name": "EUR_UKBB", "beta": -0.1165, "se": 0.0544,
             "source": "Wang 2022, UK Biobank MR-IVW, OR=0.89 (0.80-0.99)"},
            {"name": "EAS_BBJ", "beta": -0.1165, "se": 0.0684,
             "source": "Wang 2022, Biobank Japan MR-IVW, OR=0.89 (0.78-1.02)"},
        ]
    },
    "triglycerides_CAD_MR": {
        "source_papers": ["Wang 2022 Genome Medicine (PMC9195360)"],
        "strata": [
            {"name": "EUR_UKBB", "beta": 0.2390, "se": 0.1075,
             "source": "Wang 2022, UK Biobank MR-IVW, OR=1.27 (1.03-1.57)"},
            {"name": "EAS_BBJ", "beta": 0.3646, "se": 0.1468,
             "source": "Wang 2022, Biobank Japan MR-IVW, OR=1.44 (1.08-1.92)"},
        ]
    },
    "SBP_CAD_MR": {
        "source_papers": ["Wang 2022 Genome Medicine (PMC9195360)"],
        "strata": [
            {"name": "EUR_UKBB", "beta": 0.6729, "se": 0.0726,
             "source": "Wang 2022, UK Biobank MR-IVW, OR=1.96 (1.70-2.26)"},
            {"name": "EAS_BBJ", "beta": 0.5188, "se": 0.1084,
             "source": "Wang 2022, Biobank Japan MR-IVW, OR=1.68 (1.36-2.08)"},
        ]
    },
    "T2D_CAD_MR": {
        "source_papers": ["Wang 2022 Genome Medicine (PMC9195360)"],
        "strata": [
            {"name": "EUR_UKBB", "beta": 0.0770, "se": 0.0165,
             "source": "Wang 2022, UK Biobank MR-IVW, OR=1.08 (1.05-1.12)"},
            {"name": "EAS_BBJ", "beta": 0.1222, "se": 0.0247,
             "source": "Wang 2022, Biobank Japan MR-IVW, OR=1.13 (1.08-1.19)"},
        ]
    },
    "BMI_CAD_MR": {
        "source_papers": ["Wang 2022 Genome Medicine (PMC9195360)"],
        "strata": [
            {"name": "EUR_UKBB", "beta": 0.3221, "se": 0.0333,
             "source": "Wang 2022, UK Biobank MR-IVW, OR=1.38 (1.29-1.47)"},
            {"name": "EAS_BBJ", "beta": 0.5128, "se": 0.0624,
             "source": "Wang 2022, Biobank Japan MR-IVW, OR=1.67 (1.48-1.89)"},
        ]
    },
    "Lp_a_CAD_MR": {
        "source_papers": ["CKB Circulation 2025 (PMC12165552)"],
        "strata": [
            {"name": "EUR_meta", "beta": -0.2485, "se": 0.0163,
             "source": "Circulation 2025, EUR MR-IVW, RR=0.78 (0.76-0.81) per 100nmol/L lower Lp(a)"},
            {"name": "EAS_CKB", "beta": -0.2485, "se": 0.0393,
             "source": "Circulation 2025, CKB MR-IVW, RR=0.78 (0.72-0.84) per 100nmol/L lower Lp(a)"},
        ]
    },
    "BMI_depression_MR": {
        "source_papers": ["O'Loughlin 2023 BMC Medicine (PMC9893684)", "Tyrrell 2019"],
        "strata": [
            {"name": "EUR_UKBB", "beta": 0.1655, "se": 0.0410,
             "source": "Tyrrell 2019 Table 2, EUR MR-IVW, OR=1.18 (1.09-1.28) per SD BMI"},
            {"name": "EAS_meta", "beta": -0.0408, "se": 0.0134,
             "source": "O'Loughlin 2023, EAS MR-IVW, OR=0.96 (0.93-0.98) per unit BMI"},
        ]
    },
    "smoking_schizophrenia_MR": {
        "source_papers": ["Wootton 2020 Psychol Med (PMC7610182)", "Su 2022 Schizophrenia (PMC9463183)"],
        "strata": [
            {"name": "EUR_PGC", "beta": 0.4253, "se": 0.0647,
             "source": "Wootton 2020 Table 1, EUR smoking initiation IVW, OR=1.53 (1.35-1.74), 371 SNPs, PGC SCZ"},
            {"name": "EAS_TaiwanBBJ", "beta": 1.3863, "se": 0.7672,
             "source": "Su 2022, EAS smoking initiation IVW, OR=4.00 (0.89-18.01), p=0.071, Taiwan Biobank + BBJ"},
        ]
    },
    "IL6R_CAD_MR": {
        "source_papers": ["Wang 2022 IL6R MVP PheWAS (medrxiv 2022.09.24.22280325)"],
        "strata": [
            {"name": "EUR_MVP", **dict(zip(["beta", "se"], or_to_beta_se(0.96, 0.95, 0.97))),
             "source": "Wang 2022, EUR MVP PheWAS rs2228145, IHD OR=0.96 (0.95-0.97), N=439K"},
            {"name": "AFR_MVP", **dict(zip(["beta", "se"], or_to_beta_se(0.99, 0.95, 1.02))),
             "source": "Wang 2022, AFR MVP PheWAS rs2228145, IHD OR=0.99 (0.95-1.02), N=106K"},
        ]
    },
    "BMI_T2D_MR": {
        "source_papers": ["Hemani 2025 CAMeRa (doi:10.21203/rs.3.rs-6091701/v1)"],
        "strata": [
            {"name": "EUR_UKBB", "beta": 0.99, "se": 0.07,
             "source": "Hemani 2025 Fig 3 + text p8, EUR IVW logOR per SD BMI, strategy C (FEMA instruments)"},
            {"name": "EAS_BBJ", "beta": 0.66, "se": 0.08,
             "source": "Hemani 2025 Fig 3 + text p8, EAS (BBJ) IVW logOR per SD BMI, Q p=0.002"},
        ]
    },
    "LDL_stroke_MR": {
        "source_papers": ["Hemani 2025 CAMeRa (doi:10.21203/rs.3.rs-6091701/v1)"],
        "strata": [
            {"name": "EUR", "beta": 0.0811, "se": 0.0185,
             "source": "Hemani 2025 analysis repo mr.html, EUR IVW LDL→any stroke, FEMA instruments"},
            {"name": "EAS", "beta": 0.0221, "se": 0.0272,
             "source": "Hemani 2025 analysis repo mr.html, EAS IVW LDL→any stroke, FEMA instruments"},
            {"name": "AFR", "beta": 0.2852, "se": 0.0826,
             "source": "Hemani 2025 analysis repo mr.html, AFR IVW LDL→any stroke, FEMA instruments"},
            {"name": "AMR", "beta": 0.3016, "se": 0.2049,
             "source": "Hemani 2025 analysis repo mr.html, AMR IVW LDL→any stroke, FEMA instruments"},
            {"name": "SAS", "beta": 0.2061, "se": 0.1778,
             "source": "Hemani 2025 analysis repo mr.html, SAS IVW LDL→any stroke, FEMA instruments"},
        ],
        "heterogeneity_note": "5-ancestry Q=12.09, p=0.017 (non-transport). "
                              "EUR vs EAS only: Q=3.21, p=0.073 (transport). "
                              "Driven by AFR (Qj=6.66, p=0.010)."
    },
    "BMI_breast_cancer_MR": {
        "source_papers": [
            "Ooi 2019 Int J Epidemiol (PMC6659372)",
            "Wu 2025 Medicine Baltimore (PMID 40587687)",
        ],
        "assembled_pair_note": "Two independent single-ancestry MR papers, not one multi-ancestry study. "
                               "EUR from BCAC (228,951), EAS from PheWAS (159 outcomes). "
                               "Same direction (protective), Q=2.25, p=0.13.",
        "strata": [
            {"name": "EUR_BCAC", "beta": -0.2107, "se": 0.0471,
             "source": "Ooi 2019, EUR BCAC IVW, OR=0.81 (0.74-0.89)"},
            {"name": "EAS_PheWAS", "beta": -0.4005, "se": 0.1175,
             "source": "Wu 2025, EAS PheWAS IVW, OR=0.67 (0.53-0.84)"},
        ]
    },
}

ALCOHOL_MVP = {
    "source_papers": ["Kember 2024 Alcohol Clin Exp Res (DOI: 10.1111/acer.15445)"],
    "strata": [
        {"name": "EUR_MVP", **dict(zip(["beta", "se"], or_to_beta_se(1.02, 1.00, 1.05))),
         "source": "Kember 2024, EUR ADH1B 2SLS MR, OR=1.02 (1.00-1.05)"},
        {"name": "AFR_MVP", **dict(zip(["beta", "se"], or_to_beta_se(1.01, 0.96, 1.07))),
         "source": "Kember 2024, AFR ADH1B 2SLS MR, OR=1.01 (0.96-1.07)"},
        {"name": "HISP_MVP", **dict(zip(["beta", "se"], or_to_beta_se(1.04, 0.99, 1.09))),
         "source": "Kember 2024, HISP ADH1B 2SLS MR, OR=1.04 (0.99-1.09)"},
    ],
    "reclassification_note": "Real MVP data shows homogeneous null effects across all 3 ancestries (Q~0.7). "
                             "Original non-transport label was based on incomparable instruments (Holmes 2014 EUR ADH1B vs Millwood 2019 EAS ADH1B/ALDH2). "
                             "With consistent instruments from MVP, this pair shows TRANSPORT (homogeneous nulls)."
}


EXPECTED_TIER1_COUNT = 14  # 13 REPLACEMENTS + 1 ALCOHOL_MVP
EXPECTED_TOTAL_PAIRS = 71  # 14 Tier1 + 27 Tier2 + 24 Tier3 + 6 exact
assert len(REPLACEMENTS) + 1 == EXPECTED_TIER1_COUNT, (
    f"Tier 1 count drift: {len(REPLACEMENTS)} REPLACEMENTS + 1 ALCOHOL = "
    f"{len(REPLACEMENTS) + 1}, expected {EXPECTED_TIER1_COUNT}"
)


def main():
    input_path = DATA_DIR / "pairs_curated.json"
    output_path = DATA_DIR / "pairs_curated_real_data.json"

    with open(input_path) as f:
        pairs = json.load(f)

    assert len(pairs) == EXPECTED_TOTAL_PAIRS, (
        f"Total pair count drift: {len(pairs)}, expected {EXPECTED_TOTAL_PAIRS}"
    )

    original = copy.deepcopy(pairs)
    replaced = []
    reclassified = []

    for pair in pairs:
        pid = pair["id"]

        if pid in REPLACEMENTS:
            repl = REPLACEMENTS[pid]
            old_strata = pair["strata"]
            pair["strata"] = repl["strata"]
            pair["source_papers"] = repl["source_papers"]
            pair["data_provenance"] = "real_published_mr"
            replaced.append(pid)
            print(f"REPLACED {pid}: {len(old_strata)} strata -> {len(repl['strata'])} strata (all exact)")

        elif pid == "alcohol_CAD_MR":
            old_strata = pair["strata"]
            pair["strata"] = ALCOHOL_MVP["strata"]
            pair["source_papers"] = ALCOHOL_MVP["source_papers"]
            pair["data_provenance"] = "real_published_mr"
            pair["reclassification_note"] = ALCOHOL_MVP["reclassification_note"]
            replaced.append(pid)
            reclassified.append(pid)
            print(f"REPLACED {pid}: {len(old_strata)} strata -> {len(ALCOHOL_MVP['strata'])} strata (all exact)")
            print(f"  NOTE: Real data contradicts non-transport label. See reclassification_note.")

    with open(output_path, "w") as f:
        json.dump(pairs, f, indent=2)

    print(f"\nSummary: {len(replaced)} pairs replaced with real published data")
    print(f"Reclassification needed: {reclassified}")
    print(f"Output: {output_path}")

    remaining_approx = 0
    total_approx_strata = 0
    for pair in pairs:
        approx = sum(1 for s in pair.get("strata", []) if s.get("approximate", False))
        if approx > 0:
            remaining_approx += 1
            total_approx_strata += approx

    print(f"\nRemaining pairs with approximate strata: {remaining_approx}/{len(pairs)}")
    print(f"Total approximate strata remaining: {total_approx_strata}")


if __name__ == "__main__":
    main()
