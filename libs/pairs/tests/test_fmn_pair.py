import pytest
from ...int_variants.factorized_int_by_dict import FactorizedIntByDict
from ..fmn_pair import FmnPair


@pytest.mark.parametrize("m, n", [
    (7, 2),
    (3, 5),
    (15, 20),
    (25, 30),
])
def test_factorize(m, n):
    pair = FmnPair(m, n)
    assert pair.factorize() == FactorizedIntByDict.parse(m * n * (m - n) * (m + n))


@pytest.mark.parametrize("m, n", [
    (7, 2),
    (10, 10),
    (3, 5),
    (15, 20),
    (25, 30),
])
def test_value(m, n):
    pair = FmnPair(m, n)
    assert pair.value() == m * n * (m - n) * (m + n)


@pytest.mark.parametrize("m, n, expected_m, expected_n", [
    (3, 4, 7, -1),
    (5, 3, 8, 2),
    (10, 5, 15, 5),
])
def test_R2(m, n, expected_m, expected_n):
    pair = FmnPair(m, n)
    new_pair = pair.R2()
    assert new_pair.m == expected_m
    assert new_pair.n == expected_n


@pytest.mark.parametrize("m, n, expected_m, expected_n", [
    (2, 3, 4, 5),
    (4, 1, 8, 5),
    (6, 2, 12, 8),
])
def test_F1(m, n, expected_m, expected_n):
    pair = FmnPair(m, n)
    new_pair = pair.F1()
    assert new_pair.m == expected_m
    assert new_pair.n == expected_n


@pytest.mark.parametrize("m, n, expected_m, expected_n", [
    (4, 2, 8, 2),
    (6, 3, 12, 3),
    (10, 5, 20, 5),
])
def test_F2(m, n, expected_m, expected_n):
    pair = FmnPair(m, n)
    new_pair = pair.F2()
    assert new_pair.m == expected_m
    assert new_pair.n == expected_n


@pytest.mark.parametrize("m, n, expected_value", [
    # F7(m, n) = fmn(c(m, n), 4 * f(m, n)) = fmn((mm + nn)^2, 4 * m * n * (m - n) * (m + n)) = 
    # = fmn(mmmm + 2mmnn + nnnn, 4mmmn - 4mnnn) = 
    # = (mmmm + 2mmnn + nnnn) * (4mmmn - 4mnnn) * (mmmm + 2mmnn + nnnn + 4mmmn - 4mnnn) * (mmmm + 2mmnn + nnnn + 4mnnn - 4mmmn) =
    # = 4mn * (mm + nn)^2 * (m - n) * (m + n) * (2mn - (mm - nn))^2 * (2mn + (mm - nn))^2
    (3, 4, 4 * 3 * 4 * (9 + 16) ** 2 * (2 * 3 * 4 - (9 - 16)) ** 2 * (2 * 3 * 4 + (9 - 16)) ** 2),  
    (5, 6, 4 * 5 * 6 * (25 + 36) ** 2 * (2 * 5 * 6 - (25 - 36)) ** 2 * (2 * 5 * 6 + (25 - 36)) ** 2),
    (7, 8, 4 * 7 * 8 * (49 + 64) ** 2 * (2 * 7 * 8 - (49 - 64)) ** 2 * (2 * 7 * 8 + (49 - 64)) ** 2),
])
def test_F7(m, n, expected_value):
    pair = FmnPair(m, n)
    value = pair.F7().value()
    assert value == expected_value


@pytest.mark.parametrize("m, n, expected_m, expected_n", [
    (6, 4, 3, 2),
    (8, 4, 2, 1),
    (10, 5, 2, 1),
])
def test_simplify(m, n, expected_m, expected_n):
    pair = FmnPair(m, n)
    simplified_pair = pair.simplify()
    assert simplified_pair.m == expected_m
    assert simplified_pair.n == expected_n

