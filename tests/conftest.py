# MIT License © 2025 Motohiro Suzuki
from __future__ import annotations

import sys
from pathlib import Path

# Force Stage187 repo root to the front of sys.path.
# This prevents local machine contamination from other stage folders
# (e.g., stage178 editable installs) during pytest collection.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
