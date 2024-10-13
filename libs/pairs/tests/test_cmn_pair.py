import pytest

from ..cmn_pair import CmnPair


@pytest.mark.parametrize("m, n", [
    (3, 4),
    (5, 6),
    (7, 8),
])
def test_cmn_pair(m, n):
    pair = CmnPair(m, n)
    assert pair.value() == (m ** 2 + n ** 2) ** 2
