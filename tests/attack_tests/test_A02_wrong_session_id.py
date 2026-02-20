# MIT License © 2025 Motohiro Suzuki
import pytest

from qsp.protocol import ProtocolState
from qsp.errors import WrongSession

ATTACK_ID = "A02"
CLAIM_ID = "A2"
CATEGORY = "binding"


def test_A02_wrong_session_id_rejected_fail_closed():
    st = ProtocolState(session_id="S1")

    st.recv_message(session_id="S1")
    assert st.closed is False

    with pytest.raises(WrongSession):
        st.recv_message(session_id="S2")

    assert st.closed is True
