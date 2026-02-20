# MIT License © 2025 Motohiro Suzuki
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set, Tuple
import re
import sys
import yaml


ROOT = Path(__file__).resolve().parents[1]
ATTACK_TEST_DIR = ROOT / "tests" / "attack_tests"


@dataclass(frozen=True)
class Attack:
    id: str
    name: str
    category: str
    claim: str
    test_file: str


def _load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_claim_ids() -> Set[str]:
    data = _load_yaml(ROOT / "claims.yaml")
    return {str(c["id"]) for c in data.get("claims", [])}


def load_attacks() -> List[Attack]:
    data = _load_yaml(ROOT / "attack_catalog.yaml")
    attacks = []
    for a in data.get("attacks", []):
        attacks.append(
            Attack(
                id=str(a["id"]),
                name=str(a["name"]),
                category=str(a["category"]),
                claim=str(a["claim"]),
                test_file=str(a["test_file"]),
            )
        )
    return attacks


META_RE = re.compile(r'^(ATTACK_ID|CLAIM_ID|CATEGORY)\s*=\s*"([^"]+)"\s*$', re.MULTILINE)


def parse_test_metadata(test_path: Path) -> Dict[str, str]:
    txt = test_path.read_text(encoding="utf-8")
    found = dict(META_RE.findall(txt))
    return {k: v for (k, v) in found.items()}


def fail(msg: str) -> None:
    print(f"[FAIL] {msg}")
    sys.exit(1)


def ok(msg: str) -> None:
    print(f"[OK] {msg}")


def main() -> None:
    claim_ids = load_claim_ids()
    if not claim_ids:
        fail("No claims found in claims.yaml")

    attacks = load_attacks()
    if not attacks:
        fail("No attacks found in attack_catalog.yaml")

    # 1) Attack->Claim must reference existing claims; attack IDs unique
    attack_ids = [a.id for a in attacks]
    if len(set(attack_ids)) != len(attack_ids):
        fail("Duplicate attack id in attack_catalog.yaml")

    for a in attacks:
        if a.claim not in claim_ids:
            fail(f"Attack {a.id} maps to unknown claim {a.claim}")
        tf = ROOT / a.test_file
        if not tf.exists():
            fail(f"Missing test_file for attack {a.id}: {a.test_file}")

    ok("attack_catalog.yaml references valid claims and existing test files")

    # 2) Discover actual test_*.py under tests/attack_tests
    discovered = sorted(ATTACK_TEST_DIR.glob("test_*.py"))
    if not discovered:
        fail("No tests found in tests/attack_tests")

    # 3) Every catalog entry must have correct metadata inside test
    catalog_by_test = {str((ROOT / a.test_file).resolve()): a for a in attacks}

    # Ensure no extra tests exist that are not in catalog
    catalog_test_paths = {Path(ROOT / a.test_file).resolve() for a in attacks}
    discovered_paths = {p.resolve() for p in discovered}
    extra = discovered_paths - catalog_test_paths
    missing = catalog_test_paths - discovered_paths
    if extra:
        fail(f"Extra attack tests not listed in attack_catalog.yaml: {sorted(str(x) for x in extra)}")
    if missing:
        fail(f"Catalog references tests that do not exist: {sorted(str(x) for x in missing)}")

    ok("catalog <-> discovered attack tests set matches")

    # Metadata checks + 1:1 mapping constraints
    covered_claims: Dict[str, List[str]] = {cid: [] for cid in claim_ids}

    for tp in discovered:
        meta = parse_test_metadata(tp)
        for key in ("ATTACK_ID", "CLAIM_ID", "CATEGORY"):
            if key not in meta:
                fail(f"Missing {key} in {tp}")

        a = catalog_by_test[str(tp.resolve())]

        if meta["ATTACK_ID"] != a.id:
            fail(f"ATTACK_ID mismatch in {tp}: file={meta['ATTACK_ID']} catalog={a.id}")
        if meta["CLAIM_ID"] != a.claim:
            fail(f"CLAIM_ID mismatch in {tp}: file={meta['CLAIM_ID']} catalog={a.claim}")
        if meta["CATEGORY"] != a.category:
            fail(f"CATEGORY mismatch in {tp}: file={meta['CATEGORY']} catalog={a.category}")

        covered_claims[a.claim].append(a.id)

    # 4) Each Claim must be covered by >=1 attack test
    uncovered = [cid for cid, aids in covered_claims.items() if len(aids) == 0]
    if uncovered:
        fail(f"Uncovered claims (no attack tests): {uncovered}")

    ok("All claims are covered by >=1 attack test")

    # 5) Each attack maps to exactly one claim already enforced by schema;
    # additionally ensure catalog has no duplicate test_file
    test_files = [a.test_file for a in attacks]
    if len(set(test_files)) != len(test_files):
        fail("Duplicate test_file in attack_catalog.yaml")

    ok("Attack-Driven CI invariants satisfied")


if __name__ == "__main__":
    main()
