#!/usr/bin/env bash
set -euo pipefail

echo "=== Reproducing sheaf Q transportability results ==="
echo ""

cd "$(dirname "$0")"

echo "[1/3] Installing mr-transport..."
uv pip install -e ".[dev,plot]" --quiet

echo "[2/3] Running Q-test pipeline (71 pairs, 6 domains)..."
uv run python experiments/batch3_expansion/01_systematic_mr/pipeline.py --plot --sensitivity

echo "[3/3] Running sensitivity simulations (batch 4)..."
if [ -d experiments/batch4_sensitivity ]; then
    for script in experiments/batch4_sensitivity/*.py; do
        [ -f "$script" ] && uv run python "$script"
    done
fi

echo ""
echo "=== Done. Results in experiments/batch3_expansion/01_systematic_mr/results/ ==="
