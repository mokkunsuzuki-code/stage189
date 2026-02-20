# MIT License © 2025 Motohiro Suzuki
import pytest

from qsp.protocol import ProtocolState
from qsp.errors import RekeyRaceError

ATTACK_ID = "A06"
CLAIM_ID = "A6"
CATEGORY = "rekey"


def test_A06_rekey_race_double_start_rejected_fail_closed():
    st = ProtocolState(session_id="S1")

    st.start_rekey()
    assert st.closed is False

    with pytest.raises(RekeyRaceError):
        st.start_rekey()  # double start

    assert st.closed is True
