# MIT License © 2025 Motohiro Suzuki
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List
import json
import subprocess
import sys
import time
import yaml

from tools.md_table import md_table


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out" / "reports"
OUT.mkdir(parents=True, exist_ok=True)


@dataclass(frozen=True)
class Claim:
    id: str
    title: str
    description: str


@dataclass(frozen=True)
class Attack:
    id: str
    name: str
    category: str
    claim: str
    test_file: str


def run(cmd: List[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return p.returncode, p.stdout


def load_claims() -> List[Claim]:
    data = yaml.safe_load((ROOT / "claims.yaml").read_text(encoding="utf-8"))
    out: List[Claim] = []
    for c in data["claims"]:
        out.append(Claim(id=str(c["id"]), title=str(c["title"]), description=str(c["description"])))
    return out


def load_attacks() -> List[Attack]:
    data = yaml.safe_load((ROOT / "attack_catalog.yaml").read_text(encoding="utf-8"))
    out: List[Attack] = []
    for a in data["attacks"]:
        out.append(
            Attack(
                id=str(a["id"]),
                name=str(a["name"]),
                category=str(a["category"]),
                claim=str(a["claim"]),
                test_file=str(a["test_file"]),
            )
        )
    return out


def main() -> None:
    ts = int(time.time())

    lint_rc, lint_out = run([sys.executable, "tools/lint_attack_driven_ci.py"])
    test_rc, test_out = run([sys.executable, "-m", "pytest", "-q"])

    claims = load_claims()
    attacks = load_attacks()

    # Coverage table: Claim -> Attacks
    claim_to_attacks: Dict[str, List[str]] = {c.id: [] for c in claims}
    for a in attacks:
        claim_to_attacks[a.claim].append(a.id)

    md_rows = []
    for c in claims:
        md_rows.append([c.id, c.title, ", ".join(sorted(claim_to_attacks[c.id]))])

    attacks_rows = []
    for a in attacks:
        attacks_rows.append([a.id, a.category, a.claim, a.name])

    overall_pass = (lint_rc == 0) and (test_rc == 0)

    md = []
    md.append("# audit_summary (Stage187)\n")
    md.append(f"- timestamp: {ts}\n")
    md.append(f"- lint: {'PASS' if lint_rc == 0 else 'FAIL'}\n")
    md.append(f"- tests: {'PASS' if test_rc == 0 else 'FAIL'}\n")
    md.append(f"- overall: {'PASS' if overall_pass else 'FAIL'}\n\n")

    md.append("## Claim → Attack coverage\n")
    md.append(md_table(["Claim", "Title", "Covered by attacks"], md_rows))
    md.append("\n## Attack catalog (Category → Claim)\n")
    md.append(md_table(["Attack", "Category", "Claim", "Name"], attacks_rows))

    md.append("\n## Lint output\n")
    md.append("```text\n" + lint_out.strip() + "\n```\n")

    md.append("\n## Pytest output\n")
    md.append("```text\n" + test_out.strip() + "\n```\n")

    (OUT / "audit_summary.md").write_text("".join(md), encoding="utf-8")

    js = {
        "timestamp": ts,
        "lint": {"rc": lint_rc, "pass": lint_rc == 0},
        "tests": {"rc": test_rc, "pass": test_rc == 0},
        "overall_pass": overall_pass,
        "claims": [{"id": c.id, "title": c.title} for c in claims],
        "attacks": [{"id": a.id, "category": a.category, "claim": a.claim, "name": a.name} for a in attacks],
        "coverage": {cid: sorted(aids) for cid, aids in claim_to_attacks.items()},
    }
    (OUT / "audit_summary.json").write_text(json.dumps(js, indent=2, ensure_ascii=False), encoding="utf-8")

    print("[OK] wrote out/reports/audit_summary.md and audit_summary.json")
    sys.exit(0 if overall_pass else 1)


if __name__ == "__main__":
    main()
