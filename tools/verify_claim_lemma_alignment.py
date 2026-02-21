# MIT License © 2025 Motohiro Suzuki

import yaml
import sys
import re
import os

MODEL_FILE = os.environ.get("QSP_TAMARIN_MODEL", "model/qsp_state.spthy")

def extract_lemmas(path: str):
    with open(path) as f:
        content = f.read()
    return set(re.findall(r'lemma\s+(\w+)', content))

def main():
    claims_path = "claims/formal_claims.yaml"
    if not os.path.exists(claims_path):
        print("[ERROR] formal_claims.yaml not found:", claims_path)
        sys.exit(1)

    with open(claims_path) as f:
        data = yaml.safe_load(f)

    if not os.path.exists(MODEL_FILE):
        print(f"[SKIP] Tamarin model not found: {MODEL_FILE}")
        print("[SKIP] Set QSP_TAMARIN_MODEL to point to the model file to enable lemma checks.")
        print("[SKIP] Claim file is present and parsed OK.")
        return 0

    lemmas = extract_lemmas(MODEL_FILE)
    errors = 0

    for claim in data.get("claims", []):
        lemma_id = claim.get("lemma_id")
        cid = claim.get("id", "(no-id)")

        if not lemma_id:
            print(f"[FAIL] {cid} missing lemma_id field")
            errors += 1
            continue

        if lemma_id not in lemmas:
            print(f"[FAIL] {cid} -> missing lemma: {lemma_id}")
            errors += 1
        else:
            print(f"[OK] {cid} aligned with {lemma_id}")

    if errors > 0:
        print(f"[SUMMARY] {errors} alignment errors detected.")
        return 1

    print("[SUCCESS] All claims aligned with formal model.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
