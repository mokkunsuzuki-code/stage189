[![claim-alignment](https://github.com/mokkunsuzuki-code/stage189/actions/workflows/claim-alignment-ci.yml/badge.svg)](https://github.com/mokkunsuzuki-code/stage189/actions/workflows/claim-alignment-ci.yml)

# QSP Stage188 — Attack-Driven CI Audit Coverage

> Continuous, auditable verification of security claims via executable attack scenarios.

Stage188 introduces **Attack-Driven CI audit coverage** to QSP.  
Each security claim is bound to concrete adversarial tests, executed automatically in CI, and rendered as an auditable coverage matrix.

---

## 🔗 Relation to Previous Stage

This stage builds upon:

- Stage187: https://github.com/mokkunsuzuki-code/stage187

Stage188 adds:

- Claim × Attack × PASS/FAIL matrix
- Coverage % calculation
- CI gate policy
- Internet-Draft documentation of verification pipeline

---

# 🎯 Objective

Transform security claims from static documentation into:

- Executable attack tests
- Continuous CI verification
- Auditable artifacts

Security claims are no longer statements —  
they are **continuously enforced properties**.

---

# 🛡 Security Claims (claims.yaml)

Each claim represents a normative security property.

| ID | Title |
|----|-------|
| A1 | Fail-closed on mismatch |
| A2 | Session binding |
| A3 | Anti-downgrade |
| A4 | Epoch monotonicity |
| A5 | Transcript uniqueness / anti-reuse |
| A6 | Rekey race safety |

Defined in:


claims.yaml


---

# ⚔ Attack Catalog (attack_catalog.yaml)

Each attack scenario:

- Maps to exactly one security claim
- Has an executable pytest test file
- Is continuously executed in CI

Example:


attack_catalog.yaml


---

# 🔬 Attack-Driven CI Pipeline

## Execution Flow

1. CI runs per-attack pytest test suites
2. PASS / FAIL results are collected
3. Coverage matrix is generated
4. CI fails if:
   - Any claim is UNCOVERED
   - Any attack test FAILS

---

## Generated Artifacts

| Artifact | Description |
|----------|------------|
| `out/reports/attack_results.yaml` | Per-attack PASS/FAIL results |
| `out/reports/audit_summary.md` | Claim-level coverage matrix |

These are produced on every commit via GitHub Actions.

---

# 📊 Example Output

Claim	Covered By Attacks	Status
A1	A01	PASS
A2	A02	PASS
A3	A03	PASS
A4	A04	PASS
A5	A05	PASS
A6	A06	PASS

Coverage: 6/6 (100.0%)


---

# 🔁 CI Gate Policy

The pipeline fails if:

1. Any claim has no mapped attack
2. Any mapped attack test fails

This guarantees:

- No undocumented security claim
- No unverified claim
- No silently broken invariant

---

# 🧠 Why This Matters

Most cryptographic repositories provide:

- Documentation
- Tests
- Claims

Stage188 binds all three:

Claim → Attack → Executable Test → CI Enforcement → Artifact

This creates a reproducible adversarial validation loop.

---

# 🧾 Internet-Draft Integration

Stage188 formally documents the Attack-Driven CI model inside:


docs/draft-qsp-stage186-00.md


This makes the verification approach:

- Reviewable
- Citable
- Reproducible

---

# 🏗 Repository Structure


claims.yaml
attack_catalog.yaml
tools/run_attack_tests.py
tools/generate_audit_summary.py
.github/workflows/stage188-ci.yml


---

# 🚀 Running Locally

Install dependencies:

```bash
pip install pytest pyyaml

Run attack tests:

python tools/run_attack_tests.py

Generate audit summary:

python tools/generate_audit_summary.py
📜 License

MIT License © 2025 Motohiro Suzuki

🔬 Research Positioning

Stage188 demonstrates:

Attack-driven verification

Continuous adversarial validation

Claim-to-test binding

Formal documentation alignment

It is intended for:

Cryptographic research

PQC / QKD hybrid systems

Security engineering pipelines

Audit-focused protocol design

📌 Status

✔ All claims covered
✔ All attacks passing
✔ CI enforced
✔ Artifacts generated
✔ I-D updated

QSP Stage188 transforms security documentation into continuously enforced adversarial guarantees.