[![claim-alignment](https://github.com/mokkunsuzuki-code/stage189/actions/workflows/claim-alignment-ci.yml/badge.svg)](https://github.com/mokkunsuzuki-code/stage189/actions/workflows/claim-alignment-ci.yml)

# QSP Stage189 — Formal-Claim Alignment Model (FCAM)

> Machine-verifiable alignment between Security Claims and Formal Lemmas, enforced in CI.

Stage189 upgrades QSP from “claims as documentation” to **claims as mechanically enforced contracts**.

Each Claim ID defined in:

    claims/formal_claims.yaml

MUST map to exactly one formal lemma ID in the Tamarin model.

If alignment breaks, CI fails.

---

## 🎯 Objective

Prevent specification drift across:

- Implementation
- Formal model (Tamarin / ProVerif)
- Internet-Draft documentation

by enforcing:

    Claim ID ↔ Lemma ID

alignment at CI time.

---

## 🧩 What Stage189 Adds

- `claims/formal_claims.yaml`
- Claim ↔ Lemma alignment verifier
- CI enforcement gate
- Internet-Draft section: Formal-Claim Alignment Model (FCAM)

---

## 🔗 Relation to Previous Stage

Builds on:

- Stage188 (Attack-Driven CI Coverage)
  https://github.com/mokkunsuzuki-code/stage188

Stage188 ensured attack evidence coverage.
Stage189 ensures formal proof alignment consistency.

---

## 🛡 Formal-Claim Alignment Model (FCAM)

Defined in:

    docs/draft-qsp-stage186-00.md

The FCAM section formally specifies:

- Claim registry structure
- Lemma binding rules
- CI failure semantics

This prevents:

- Silent divergence between code and formal model
- Informal claim inflation
- Spec drift across documentation layers

---

## 🔬 Local Verification (Optional)

If a Tamarin model exists locally:

```bash
QSP_TAMARIN_MODEL=path/to/qsp_state.spthy \
python tools/verify_claim_lemma_alignment.py

If no model is present, the script exits safely with SKIP.

📜 License

MIT License © 2025 Motohiro Suzuki