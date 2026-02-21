---
title: "QSP Stage186 - Claims Visibility and CI Evidence Model"
abbrev: "QSP-Stage186"
docname: draft-qsp-stage186-00
category: info
ipr: trust200902
submissiontype: independent
author:
 -
    ins: Motohiro Suzuki
    name: Motohiro Suzuki
    org: Independent Research
    email: (private)
---

# Abstract

This document specifies Stage186 of the Quantum-Safe Protocol (QSP).
Stage186 introduces structured Security Claim visibility and a
fail-with-evidence Continuous Integration (CI) model.

The primary contribution of this stage is not cryptographic innovation,
but explicit attack-model articulation and evidence-preserving CI behavior.

# Status of This Memo

This Internet-Draft is provided for independent review and documentation.
It is not an IETF working group document.

# 1. Introduction

QSP is a structured hybrid protocol framework targeting lifecycle clarity,
fail-closed semantics, and attack-surface reduction.

Stage186 formalizes:

- Security Claims (A1–A5)
- Artifact-preserving CI
- Explicit attack-model categorization
- Declared non-goals

# 2. Terminology

- **Epoch**: A strictly increasing lifecycle version identifier.
- **Handshake**: Session establishment phase.
- **Fail-closed**: Terminate immediately on validation failure.
- **Matrix**: CI validation execution (docker or pytest fallback).
- **Artifact**: CI-generated log, summary, or machine-readable exit code.

# 3. Declared Security Claims

A1 – Fail-Closed Semantics  
A2 – Handshake Gating  
A3 – Epoch Monotonicity  
A4 – Session Binding  
A5 – Key Separation  

Claims are descriptive at this stage and connected to CI visibility.

# 3. Formal-Claim Alignment Model (FCAM)

This document enforces a machine-checkable alignment between:

- Security Claims (claims/formal_claims.yaml)
- Formal lemmas (Tamarin model)
- CI enforcement

Each Claim ID MUST map to exactly one lemma_id.
CI MUST fail if any mapping becomes invalid.

This prevents specification drift across:
Implementation ↔ Formal model ↔ Internet-Draft text.

# 3. Formal-Claim Alignment Model (FCAM)

This document enforces a machine-checkable alignment between:

- Security Claims (claims/formal_claims.yaml)
- Formal lemmas (Tamarin model)
- CI enforcement

Each Claim ID MUST map to exactly one lemma_id.
CI MUST fail if any mapping becomes invalid.

This prevents specification drift across:
Implementation ↔ Formal model ↔ Internet-Draft text.

# 4. Security Considerations (Attack Model Classification)

This section explicitly defines attack categories and Stage186 behavior.

---

## 4.1 Replay Attacks

Threat:
An attacker replays previously valid protocol messages.

Mitigation Scope:
- Epoch monotonicity (A3) conceptually prevents rollback.
- CI preserves logs for replay scenario inspection.

Limitations:
- No formal replay proof is included in Stage186.

---

## 4.2 Epoch Rollback / Regression

Threat:
Forcing the protocol to accept a previous lifecycle state.

Mitigation Scope:
- Epoch MUST increase (A3).
- CI matrix ensures visible failure if logic breaks.

Limitations:
- Enforcement depends on future implementation integration.

---

## 4.3 Session Mix-Up

Threat:
Messages from one session are accepted in another context.

Mitigation Scope:
- Session Binding claim (A4).
- Documented as invariant in claims table.

Limitations:
- No symbolic proof integrated in this stage.

---

## 4.4 Pre-Handshake Injection

Threat:
Application data accepted before authentication.

Mitigation Scope:
- Handshake Gating claim (A2).
- CI ensures invariant breakage produces artifacts.

---

## 4.5 Key Reuse / Cross-Epoch Leakage

Threat:
Key material reused across epochs or contexts.

Mitigation Scope:
- Key Separation claim (A5).
- Explicit documentation of separation requirement.

---

## 4.6 Downgrade Attacks

Threat:
Forcing weaker operational mode.

Mitigation Scope:
- Fail-closed semantics (A1).
- CI ensures downgrade failure is logged.

Limitations:
- No cryptographic downgrade detection proof provided.

---

## 4.7 CI Bypass Risks

Threat:
Failure occurs but CI hides or overwrites evidence.

Mitigation Scope:
- `matrix.exit` machine-readable result.
- Mandatory artifact upload.
- Summary gate enforcement.

Stage186 explicitly defends against silent CI failure.

---

## 4.8 Artifact Tampering

Threat:
Generated logs are modified or lost.

Mitigation Scope:
- GitHub artifact immutability.
- Deterministic exit codes.

Out of Scope:
- External artifact integrity proof.

---

# 5. Non-Goals

Stage186 does NOT:

- Provide formal symbolic proofs.
- Introduce new cryptographic primitives.
- Guarantee quantum attack resistance.
- Modify handshake internals.

# 6. Implementation Status

Implemented components:

- CI workflow: `.github/workflows/stage186-ci.yml`
- Matrix runner: `tools/ci_run_matrix.sh`
- Pytest fallback: `tools/ci_matrix_pytest.sh`
- Claims table: `claims/CLAIMS.md`
- Smoke tests: `tests/test_stage186_smoke.py`

# 7. IANA Considerations

No IANA actions required.

# 8. Conclusion

Stage186 transitions QSP from informal documentation to
attack-aware structured specification with evidence-preserving CI.

The stage prioritizes reviewer transparency over cryptographic novelty.


## Attack-Driven CI Verification

QSP includes an automated Attack-Driven CI pipeline that continuously verifies
security claims against concrete, reproducible attack scenarios.

### Inputs

- `claims.yaml`: normative list of security claims (A1–A6)
- `attack_catalog.yaml`: mapping of each attack scenario to the claim it validates,
  including the executable test file

### Outputs

- `out/reports/attack_results.yaml`: per-attack PASS/FAIL results from CI execution
- `out/reports/audit_summary.md`: claim-level coverage matrix and status

### CI Gate Policy

The CI pipeline MUST fail if either condition holds:

1. Any claim is UNCOVERED (no mapped attack scenario).
2. Any mapped attack scenario fails (FAIL).

This provides a continuously verifiable binding from security claims to executable
adversarial tests, producing auditable evidence on every commit.

