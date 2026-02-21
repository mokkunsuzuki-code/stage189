# MIT License © 2025 Motohiro Suzuki
from __future__ import annotations

import subprocess
from pathlib import Path
import yaml

CATALOG = "attack_catalog.yaml"
OUT = "out/reports/attack_results.yaml"


def load_catalog() -> list[dict]:
    doc = yaml.safe_load(Path(CATALOG).read_text(encoding="utf-8")) or {}
    attacks = doc.get("attacks", [])
    if not isinstance(attacks, list) or not attacks:
        raise ValueError("attack_catalog.yaml must contain non-empty 'attacks:' list.")
    return attacks


def run_pytest(test_file: str) -> tuple[bool, str]:
    # Run a single file; keep output for debugging.
    cmd = ["python", "-m", "pytest", "-q", test_file]
    p = subprocess.run(cmd, text=True, capture_output=True)
    ok = (p.returncode == 0)
    out = (p.stdout or "") + (p.stderr or "")
    # Truncate noisy output to keep artifact readable
    if len(out) > 8000:
        out = out[:8000] + "\n...[truncated]..."
    return ok, out.strip()


def main() -> int:
    attacks = load_catalog()

    results = {"attacks": []}
    any_fail = False

    for a in attacks:
        aid = a.get("id", "")
        test_file = a.get("test_file", "")
        claim = a.get("claim", "")

        if not test_file:
            results["attacks"].append(
                {"id": aid, "claim": claim, "test_file": test_file, "status": "UNKNOWN", "note": "no test_file"}
            )
            continue

        tf = Path(test_file)
        if not tf.exists():
            any_fail = True
            results["attacks"].append(
                {"id": aid, "claim": claim, "test_file": test_file, "status": "FAIL", "note": "missing test file"}
            )
            continue

        ok, log = run_pytest(test_file)
        status = "PASS" if ok else "FAIL"
        if not ok:
            any_fail = True

        results["attacks"].append(
            {"id": aid, "claim": claim, "test_file": test_file, "status": status, "log": log}
        )

    Path("out/reports").mkdir(parents=True, exist_ok=True)
    Path(OUT).write_text(yaml.safe_dump(results, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"[OK] wrote {OUT}")

    return 1 if any_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
