# MIT License © 2025 Motohiro Suzuki
import pytest

from qsp.protocol import ProtocolState
from qsp.errors import DowngradeDetected

ATTACK_ID = "A03"
CLAIM_ID = "A3"
CATEGORY = "downgrade"


def test_A03_downgrade_is_rejected_fail_closed():
    st = ProtocolState(session_id="S1")

    st.negotiate("PQC+QKD")
    assert st.closed is False

    with pytest.raises(DowngradeDetected):
        st.negotiate("PQC-only")

    assert st.closed is True
