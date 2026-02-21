[![claim-alignment](https://github.com/mokkunsuzuki-code/stage189/actions/workflows/claim-alignment-ci.yml/badge.svg)](https://github.com/mokkunsuzuki-code/stage189/actions/workflows/claim-alignment-ci.yml)
# QSP Stage189 — Formal-Claim Alignment Model (FCAM)

> Machine-verifiable alignment between Security Claims and Formal Lemmas, enforced in CI.

Stage189 upgrades QSP from “claims as documentation” to **claims as mechanically enforced contracts**.
Each Claim ID in `claims/formal_claims.yaml` maps to a lemma ID in the Tamarin model, and CI fails on drift.

---

## 🔗 Relation to Previous Stage

This stage builds upon:

- Stage188: https://github.com/mokkunsuzuki-code/stage188

Stage189 adds:

- `formal_claims.yaml` (Claim ↔ Lemma binding)
- Claim–Lemma alignment verifier (CI gate)
- Internet-Draft section text: FCAM

---

## 🎯 Objective

Prevent specification drift across:

- Implementation
- Formal model (Tamarin/ProVerif)
- Internet-Draft text

by enforcing **Claim ID ↔ Lemma ID** alignment in CI.

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
