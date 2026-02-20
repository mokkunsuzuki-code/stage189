# MIT License © 2025 Motohiro Suzuki
class QSPError(Exception):
    """Base error for QSP."""


class RejectError(QSPError):
    """Raised when an input is rejected and the protocol should fail-closed."""


class DowngradeDetected(RejectError):
    """Raised when a downgrade attempt is detected."""


class WrongSession(RejectError):
    """Raised when session binding fails."""


class EpochError(RejectError):
    """Raised when epoch monotonicity is violated."""


class ReplayDetected(RejectError):
    """Raised when replay is detected."""


class RekeyRaceError(RejectError):
    """Raised when rekey race is detected."""
