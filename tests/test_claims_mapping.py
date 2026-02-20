# MIT License © 2025 Motohiro Suzuki
from __future__ import annotations

from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_catalog_claims_are_consistent():
    claims = yaml.safe_load((ROOT / "claims.yaml").read_text(encoding="utf-8"))["claims"]
    claim_ids = {c["id"] for c in claims}

    catalog = yaml.safe_load((ROOT / "attack_catalog.yaml").read_text(encoding="utf-8"))["attacks"]
    for a in catalog:
        assert a["claim"] in claim_ids, f"Attack {a['id']} maps to unknown claim {a['claim']}"
        assert (ROOT / a["test_file"]).exists(), f"Missing test_file for attack {a['id']}: {a['test_file']}"
