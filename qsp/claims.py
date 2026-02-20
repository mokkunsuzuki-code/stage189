# MIT License © 2025 Motohiro Suzuki
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import yaml


@dataclass(frozen=True)
class Claim:
    id: str
    title: str
    description: str


def load_claims_yaml(path: str | Path) -> List[Claim]:
    p = Path(path)
    data = yaml.safe_load(p.read_text(encoding="utf-8"))
    claims = data.get("claims", [])
    out: List[Claim] = []
    for c in claims:
        out.append(Claim(id=str(c["id"]), title=str(c["title"]), description=str(c["description"])))
    return out


def claims_index(claims: List[Claim]) -> Dict[str, Claim]:
    return {c.id: c for c in claims}
