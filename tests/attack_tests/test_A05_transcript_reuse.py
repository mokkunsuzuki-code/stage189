# MIT License © 2025 Motohiro Suzuki
import pytest

from qsp.protocol import ProtocolState
from qsp.errors import RejectError

ATTACK_ID = "A05"
CLAIM_ID = "A5"
CATEGORY = "transcript"


def test_A05_transcript_partial_reuse_rejected_fail_closed():
    st = ProtocolState(session_id="S1")

    st.accept_transcript_hash("H1")
    assert st.closed is False

    with pytest.raises(RejectError):
        st.accept_transcript_hash("H1")  # reuse

    assert st.closed is True
