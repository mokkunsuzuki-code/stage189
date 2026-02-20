# MIT License © 2025 Motohiro Suzuki
from __future__ import annotations

from typing import List


def md_table(headers: List[str], rows: List[List[str]]) -> str:
    def esc(s: str) -> str:
        return s.replace("\n", " ").replace("|", "\\|")

    h = "| " + " | ".join(esc(x) for x in headers) + " |"
    sep = "| " + " | ".join(["---"] * len(headers)) + " |"
    out = [h, sep]
    for r in rows:
        out.append("| " + " | ".join(esc(str(x)) for x in r) + " |")
    return "\n".join(out) + "\n"
