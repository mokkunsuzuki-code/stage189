# MIT License © 2025 Motohiro Suzuki
from __future__ import annotations

from pathlib import Path
import yaml

PREFERRED_CLAIMS = ["claims.yaml", "claims/claims_table.yaml"]
PREFERRED_ATTACKS = ["attack_catalog.yaml", "claims/attack_map.yaml"]

RESULTS_FILE = "out/reports/attack_results.yaml"
OUTPUT_FILE = "out/reports/audit_summary.md"


def load_yaml_file(candidates: list[str]) -> tuple[str, dict]:
    for path in candidates:
        p = Path(path)
        if p.exists():
            return path, (yaml.safe_load(p.read_text(encoding="utf-8")) or {})
    raise FileNotFoundError(f"Missing required YAML. Tried: {candidates}")


def normalize_claims(doc: dict) -> list[dict]:
    claims = doc.get("claims")
    if isinstance(claims, list) and claims:
        for c in claims:
            if "id" not in c:
                raise ValueError("Each claim must have 'id'.")
        return claims
    raise ValueError("Claims YAML must contain non-empty 'claims:' list.")


def normalize_attacks(doc: dict) -> list[dict]:
    attacks = doc.get("attacks")
    if not isinstance(attacks, list):
        raise ValueError("Attack YAML must contain 'attacks:' list.")

    norm: list[dict] = []
    for a in attacks:
        if not isinstance(a, dict):
            continue
        aid = a.get("id")
        if not aid:
            raise ValueError("Each attack must have 'id'.")

        validates = a.get("validates", None)
        if validates is None:
            single = a.get("claim", None)
            if isinstance(single, str) and single.strip():
                validates = [single.strip()]
            else:
                validates = []
        else:
            if isinstance(validates, str):
                validates = [validates]
            elif not isinstance(validates, list):
                validates = []

        norm.append(
            {
                "id": str(aid),
                "name": a.get("name", ""),
                "validates": [str(x).strip() for x in validates if str(x).strip()],
                "category": a.get("category", ""),
                "test_file": a.get("test_file", ""),
            }
        )
    return norm


def load_results() -> dict[str, str]:
    """
    Returns mapping: attack_id -> status (PASS/FAIL/UNKNOWN)
    """
    p = Path(RESULTS_FILE)
    if not p.exists():
        return {}
    doc = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    items = doc.get("attacks", [])
    m: dict[str, str] = {}
    if isinstance(items, list):
        for it in items:
            if isinstance(it, dict) and "id" in it and "status" in it:
                m[str(it["id"])] = str(it["status"])
    return m


def claim_status_from_attacks(attack_ids: list[str], attack_status: dict[str, str]) -> str:
    """
    Claim status rules:
      - if any mapped attack FAIL -> FAIL
      - else if any mapped attack PASS -> PASS
      - else if mapped but no results -> UNKNOWN
      - else (no mapped attacks) -> UNCOVERED
    """
    if not attack_ids:
        return "UNCOVERED"
    statuses = [attack_status.get(aid, "UNKNOWN") for aid in attack_ids]
    if any(s == "FAIL" for s in statuses):
        return "FAIL"
    if any(s == "PASS" for s in statuses):
        return "PASS"
    return "UNKNOWN"


def main() -> int:
    claims_path, claims_doc = load_yaml_file(PREFERRED_CLAIMS)
    attacks_path, attacks_doc = load_yaml_file(PREFERRED_ATTACKS)

    claims = normalize_claims(claims_doc)
    attacks = normalize_attacks(attacks_doc)
    attack_status = load_results()

    claim_ids = [c["id"] for c in claims]
    coverage_map: dict[str, list[str]] = {cid: [] for cid in claim_ids}

    for atk in attacks:
        aid = atk["id"]
        for cid in atk.get("validates", []) or []:
            if cid in coverage_map:
                coverage_map[cid].append(aid)

    covered = sum(1 for cid in coverage_map if coverage_map[cid])
    total = len(coverage_map)
    coverage_percent = round((covered / total) * 100, 1) if total else 0.0

    lines: list[str] = []
    lines.append("# Audit Coverage Summary\n")
    lines.append("## Inputs\n")
    lines.append(f"- Claims: `{claims_path}`")
    lines.append(f"- Attacks: `{attacks_path}`")
    lines.append(f"- Results: `{RESULTS_FILE}` (if present)\n")
    lines.append("| Claim | Covered By Attacks | Status |")
    lines.append("|-------|--------------------|--------|")

    any_fail = False
    any_uncovered = False

    for cid in claim_ids:
        aids = coverage_map[cid]
        attacks_list = ", ".join(aids) if aids else "-"
        status = claim_status_from_attacks(aids, attack_status)

        if status == "FAIL":
            any_fail = True
        if status == "UNCOVERED":
            any_uncovered = True

        lines.append(f"| {cid} | {attacks_list} | {status} |")

    lines.append("")
    lines.append(f"**Coverage: {covered}/{total} ({coverage_percent}%)**")
    lines.append("")

    Path("out/reports").mkdir(parents=True, exist_ok=True)
    Path(OUTPUT_FILE).write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] wrote {OUTPUT_FILE} (coverage {covered}/{total} = {coverage_percent}%)")

    # Gate: fail CI on uncovered OR failing attacks
    if any_uncovered:
        print("[FAIL] uncovered claims exist.")
        return 1
    if any_fail:
        print("[FAIL] at least one attack test failed.")
        return 1

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"[ERR] {e}")
        raise SystemExit(2)
