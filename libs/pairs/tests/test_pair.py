import pytest

from ..pair import Pair


@pytest.mark.parametrize("m, n", [
    (3, 5),
    (-3, 5),
    (3, -5),
    (-3, -5),
])
def test_pair(m, n):
    pair = Pair(m, n)
    assert pair.m == m and pair.n == n


def test_pair_eq():
    pair1 = Pair(3, 5)
    pair2 = Pair(3, 5)
    assert pair1 == pair2


def test_pair_ne():
    pair1 = Pair(3, 5)
    pair2 = Pair(3, 6)
    assert pair1 != pair2
