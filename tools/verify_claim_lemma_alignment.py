# MIT License © 2025 Motohiro Suzuki

import yaml
import sys
import re
import os

MODEL_FILE = "model/qsp_state.spthy"

def extract_lemmas():
    if not os.path.exists(MODEL_FILE):
        print("[ERROR] Model file not found:", MODEL_FILE)
        sys.exit(1)

    with open(MODEL_FILE) as f:
        content = f.read()

    return set(re.findall(r'lemma\s+(\w+)', content))

def main():
    if not os.path.exists("claims/formal_claims.yaml"):
        print("[ERROR] formal_claims.yaml not found")
        sys.exit(1)

    with open("claims/formal_claims.yaml") as f:
        data = yaml.safe_load(f)

    lemmas = extract_lemmas()
    errors = 0

    for claim in data["claims"]:
        lemma_id = claim["lemma_id"]

        if lemma_id not in lemmas:
            print(f"[FAIL] {claim['id']} -> missing lemma: {lemma_id}")
            errors += 1
        else:
            print(f"[OK] {claim['id']} aligned with {lemma_id}")

    if errors > 0:
        print(f"[SUMMARY] {errors} alignment errors detected.")
        sys.exit(1)

    print("[SUCCESS] All claims aligned with formal model.")

if __name__ == "__main__":
    main()
