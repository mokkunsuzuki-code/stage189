## Formal-Claim Alignment Model (FCAM)

This repository enforces a machine-checkable alignment between:

- Security Claims (claims/formal_claims.yaml)
- Formal lemmas (Tamarin model)
- CI enforcement

Each Claim ID MUST map to exactly one lemma_id.
CI MUST fail if any mapping becomes invalid.

This prevents specification drift across:
Implementation ↔ Formal Model ↔ Internet-Draft text.
