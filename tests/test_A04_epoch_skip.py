# MIT License © 2025 Motohiro Suzuki
import pytest

from qsp.protocol import ProtocolState
from qsp.errors import EpochError

ATTACK_ID = "A04"
CLAIM_ID = "A4"
CATEGORY = "epoch"


def test_A04_epoch_skip_or_out_of_order_rejected_fail_closed():
    st = ProtocolState(session_id="S1", epoch=1)

    # legal: 1 -> 2
    st.advance_epoch(2)
    assert st.closed is False
    assert st.epoch == 2

    # illegal: 2 -> 4 (skip)
    with pytest.raises(EpochError):
        st.advance_epoch(4)

    assert st.closed is True
