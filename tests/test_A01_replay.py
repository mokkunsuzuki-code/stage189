# MIT License © 2025 Motohiro Suzuki
import pytest

from qsp.protocol import ProtocolState
from qsp.errors import ReplayDetected

ATTACK_ID = "A01"
CLAIM_ID = "A1"
CATEGORY = "replay"


def test_A01_replay_ack_is_rejected_fail_closed():
    st = ProtocolState(session_id="S1")

    st.recv_ack(nonce="N1")
    assert st.closed is False

    with pytest.raises(ReplayDetected):
        st.recv_ack(nonce="N1")  # replay

    assert st.closed is True
