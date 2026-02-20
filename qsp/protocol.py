# MIT License © 2025 Motohiro Suzuki
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Set, Tuple

from .errors import (
    DowngradeDetected,
    EpochError,
    RekeyRaceError,
    ReplayDetected,
    RejectError,
    WrongSession,
)


@dataclass
class ProtocolState:
    """
    Minimal state machine used by Stage187 tests.

    NOTE:
    - This is intentionally small: Stage187 focuses on CI traceability
      (attack→test→claim mapping) rather than full protocol realism.
    """
    session_id: str
    epoch: int = 0
    negotiated_suite: str = "PQC+QKD"  # expected strongest suite by default
    seen_nonces: Set[str] = field(default_factory=set)
    rekey_in_progress: bool = False
    transcript_hashes: Set[str] = field(default_factory=set)

    closed: bool = False

    def _fail_closed(self, exc: RejectError) -> None:
        self.closed = True
        raise exc

    def recv_ack(self, nonce: str) -> None:
        if self.closed:
            self._fail_closed(ReplayDetected("protocol already closed"))
        if nonce in self.seen_nonces:
            self._fail_closed(ReplayDetected("replay nonce detected"))
        self.seen_nonces.add(nonce)

    def recv_message(self, session_id: str) -> None:
        if self.closed:
            self._fail_closed(WrongSession("protocol already closed"))
        if session_id != self.session_id:
            self._fail_closed(WrongSession("wrong session_id"))

    def negotiate(self, offered_suite: str) -> None:
        """
        offered_suite: e.g. "PQC+QKD" (strong) or "PQC-only" (downgrade)
        """
        if self.closed:
            self._fail_closed(DowngradeDetected("protocol already closed"))
        # Strict anti-downgrade: any weaker than "PQC+QKD" is rejected
        if offered_suite != "PQC+QKD":
            self._fail_closed(DowngradeDetected(f"downgrade detected: {offered_suite}"))
        self.negotiated_suite = offered_suite

    def advance_epoch(self, new_epoch: int) -> None:
        if self.closed:
            self._fail_closed(EpochError("protocol already closed"))
        # Must be exactly +1 for this minimal model
        if new_epoch != self.epoch + 1:
            self._fail_closed(EpochError(f"epoch violation: {self.epoch} -> {new_epoch}"))
        self.epoch = new_epoch

    def accept_transcript_hash(self, h: str) -> None:
        if self.closed:
            self._fail_closed(RejectError("protocol already closed"))
        if h in self.transcript_hashes:
            self._fail_closed(RejectError("transcript reuse detected"))
        self.transcript_hashes.add(h)

    def start_rekey(self) -> None:
        if self.closed:
            self._fail_closed(RekeyRaceError("protocol already closed"))
        if self.rekey_in_progress:
            self._fail_closed(RekeyRaceError("double rekey detected"))
        self.rekey_in_progress = True

    def finish_rekey(self) -> None:
        if self.closed:
            self._fail_closed(RekeyRaceError("protocol already closed"))
        if not self.rekey_in_progress:
            self._fail_closed(RekeyRaceError("finish_rekey without start"))
        self.rekey_in_progress = False
