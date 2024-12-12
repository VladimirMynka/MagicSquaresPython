import random
import time

import pytest

from ..factorized_int_base import FactorizedIntBase
from ..factorized_int_by_dict import FactorizedIntByDict


def test_factorized_int_initialization():
    # Test initialization with a valid list of powers
    fi = FactorizedIntByDict({2: 7, 3: 5, 7: 0})  # Represents 2^2 * 3^1 = 12
    assert fi.injections == {2: 7, 3: 5, 7: 0}


@pytest.mark.parametrize('a', [1, 2, 4, 9, 12, 15, 18, 49, 144, 10 ** 5])
def test_factorization_and_conversion(a: int):
    fi = FactorizedIntByDict.parse(a)
    assert int(fi) == a
    assert float(fi) == float(a)


def test_string_conversation():
    fi = FactorizedIntByDict.parse(2 ** 17 * 3 ** 11)
    assert str(fi) == '2¹⁷·3¹¹'

    fi = FactorizedIntByDict.parse(1)
    assert str(fi) == '1'

    fi = FactorizedIntByDict.parse(3 * 5)
    assert str(fi) == '3·5'


def test_addition():
    fi1 = FactorizedIntByDict.parse(12)  # 12 = 2^2 * 3^1
    fi2 = FactorizedIntByDict.parse(18)  # 18 = 2^1 * 3^2
    result = fi1 + fi2  # should be 30
    assert int(result) == 30


def test_subtraction():
    fi1 = FactorizedIntByDict.parse(30)  # 30
    fi2 = FactorizedIntByDict.parse(12)  # 12
    result = fi1 - fi2  # should be 18
    assert int(result) == 18


def test_multiplication():
    fi1 = FactorizedIntByDict.parse(6)  # 6 = 2^1 * 3^1
    fi2 = FactorizedIntByDict.parse(5)  # 5 = 5^1
    result = fi1 * fi2  # should be 30
    assert int(result) == 30


def test_gcd():
    fi1 = FactorizedIntByDict.parse(30)  # 30
    fi2 = FactorizedIntByDict.parse(12)  # 12
    result = fi1 & fi2  # GCD(30, 12) = 6
    assert int(result) == 6


def test_lcm():
    fi1 = FactorizedIntByDict.parse(30)  # 30
    fi2 = FactorizedIntByDict.parse(12)  # 12
    result = fi1 | fi2  # LCM(30, 12) = 60
    assert int(result) == 60


def test_exponentiation():
    fi = FactorizedIntByDict.parse(3)  # 3^1
    result = fi ** 3  # should be 27
    assert int(result) == 27


def test_normalization():
    fi = FactorizedIntByDict({2: 2, 3: 0, 7: 0, 5: 1, 17: 1})  # Represents 2^2
    normalized_fi = fi.normalize()
    assert normalized_fi.injections == {2: 2, 5: 1, 17: 1}  # Remove trailing zeros


def test_speed_parse():
    FactorizedIntByDict.primes = [2, 3, 5, 7, 11]
    start_time = time.time()
    _ = FactorizedIntByDict.parse(10 ** 11)
    assert (time.time() - start_time) < 0.5

    start_time = time.time()
    for i in range(1000):
        _ = FactorizedIntByDict.parse(10 ** 6)
    assert (time.time() - start_time) < 0.5


def test_speed_addition():
    start_time = time.time()
    for i in range(1000):
        fi1 = FactorizedIntByDict.parse(10 ** 6)
        fi2 = FactorizedIntByDict.parse(10 ** 6)
        _ = fi1 + fi2
    assert (time.time() - start_time) < 0.35


def test_speed_multiplication():
    start_time = time.time()
    for i in range(1000):
        fi1 = FactorizedIntByDict.parse(10 ** 6)
        fi2 = FactorizedIntByDict.parse(10 ** 6)
        _ = fi1 * fi2
    assert (time.time() - start_time) < 0.25


def test_speed_exponentiation():
    start_time = time.time()
    for i in range(1000):
        fi1 = FactorizedIntByDict.parse(10 ** 6)
        _ = fi1 ** 100
    assert (time.time() - start_time) < 0.25


def test_speed_big_prime():
    FactorizedIntBase.primes = [2, 3, 5, 7, 11]
    start_time = time.time()
    for i in range(100):
        a = random.randint(1000, 10000)
        fi = FactorizedIntByDict.parse(10 ** 6 * 3559 * 3571 ** 5 * 10001 ** 3 * a)
        assert int(fi) == 10 ** 6 * 3559 * 3571 ** 5 * 10001 ** 3 * a

    assert (time.time() - start_time) < 0.25


def test_speed_very_big_prime():
    FactorizedIntBase.primes = [2, 3, 5, 7, 11]

    a = 33461 ** 17 * 331777 ** 5 * 8191 ** 3

    start_time = time.time()

    fi = FactorizedIntByDict.parse(a)
    assert (time.time() - start_time) < 0.40

    assert int(fi) == a


def test_speed_many_little_primes():
    FactorizedIntBase.primes = [2, 3, 5, 7, 11]

    start_time = time.time()
    [FactorizedIntByDict.parse(i) for i in range(1, 1000) for _ in range(5)]

    assert (time.time() - start_time) < 0.25


def test_string_order():
    assert str(
        FactorizedIntByDict.parse(2 * 3 ** 3 * 11 * 17 ** 2 * 131) *
        FactorizedIntByDict.parse(13 * 23 * 29 ** 2)
    ) == '2·3³·11·13·17²·23·29²·131'

