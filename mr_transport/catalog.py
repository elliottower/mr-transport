"""Load the bundled 71-pair MR transportability catalog."""

from __future__ import annotations

import json
from importlib.resources import files
from typing import Any


def load_catalog() -> list[dict[str, Any]]:
    """Load the curated 71-pair MR catalog bundled with the package.

    Each entry has: id, exposure, outcome, domain, expected, strata.
    Strata contain: name, beta, se, source, and optionally approximate=True.

    Returns:
        List of pair dictionaries.
    """
    data_file = files("mr_transport.data").joinpath("pairs_curated.json")
    return json.loads(data_file.read_text(encoding="utf-8"))
