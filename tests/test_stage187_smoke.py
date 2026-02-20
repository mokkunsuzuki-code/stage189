# MIT License © 2025 Motohiro Suzuki
from pathlib import Path

def test_stage187_required_files_exist():
    root = Path(__file__).resolve().parents[1]

    required = [
        root / ".github" / "workflows" / "ci.yml",
        root / "tools" / "lint_attack_driven_ci.py",
        root / "tools" / "generate_audit_summary.py",
        root / "attack_catalog.yaml",
        root / "claims.yaml",
        root / "README.md",
    ]

    missing = [p.as_posix() for p in required if not p.exists()]
    assert not missing, "Missing required Stage187 files:\n" + "\n".join(missing)
